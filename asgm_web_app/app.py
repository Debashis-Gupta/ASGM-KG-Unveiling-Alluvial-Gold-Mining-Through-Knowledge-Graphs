import streamlit as st 
from graphdatascience import GraphDataScience 
import pandas as pd
from show_graph import create_vis
import streamlit.components.v1 as components
from pyvis.network import Network
from io import StringIO
import tempfile
import os
from summary import *
from llama_agent import ask_query
# Page Configuration
st.set_page_config(layout="wide")
st.markdown("""
<style>
.scrollable-div {
    height: 300px;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)
st.title('ASGM Knowledge Graph Explorer')

st.markdown("""
Welcome to the ASGM Knowledge Graph Explorer, an interactive platform designed to enhance understanding and facilitate in-depth analysis of the Artisanal and Small-scale Gold Mining sector. Here, users can visually navigate through complex data, engage in dynamic Query and Answer sessions, and generate summarized insights from the Knowledge Graph. Whether you are a researcher, policymaker, or industry stakeholder, this tool is crafted to provide you with comprehensive insights and assist in decision-making processes by presenting a clear and navigable view of interconnected data.
""")

# Connect to Neo4j
@st.cache_resource
def connect(url, user, pwd, dbname):
    return GraphDataScience(url, auth=(user, pwd), database=dbname)

neo4j_url = None
neo4j_user = None
neo4j_password = None
neo4j_database = None
neo = connect(neo4j_url,neo4j_user,neo4j_password,neo4j_database)

@st.cache_resource
def get_graph():
    query = """
    MATCH (n)-[r]->(m)
    RETURN n.name as n, TYPE(r) as r, m.name as m
    """
    return neo.run_cypher(query)

@st.cache_resource
def get_nodelist():
    query = """
    MATCH (n)
    RETURN DISTINCT n.name
    """
    return neo.run_cypher(query)
@st.cache_resource
def get_relationlist():
    query = """
    MATCH ()-[r]->()
    RETURN DISTINCT TYPE(r) AS RelationshipType
    """
    return neo.run_cypher(query)

@st.cache_resource
def get_QnA(query):
    return neo.run_cypher(query)

@st.cache_resource
def get_hop_summary(source_node,k):
    query = f"""
        MATCH path=(a)-[r*..{k}]-(b)
        WHERE a.name = $source_node
        UNWIND r as rel
        RETURN a.name as Subject, type(rel) AS Predicate, b.name as Object
        LIMIT 50
    """
    params = {"source_node":source_node}
    return neo.run_cypher(query,params=params)

@st.cache_resource
def get_hop_summary2(source_node,dest_node):
    query = f"""
        MATCH path=(a)-[r*]-(b)
        WHERE a.name = $source_node and b.name=$dest_node
        UNWIND r as rel
        RETURN a.name as Subject, type(rel) AS Predicate, b.name as Object
        LIMIT 1
    """
    params = {"source_node":source_node,"dest_node":dest_node}
    return neo.run_cypher(query,params=params)

def get_QnA_graph(graph_data):
    seen_nodes = set()
    net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black", notebook=True,directed=True)
    net.options.edges.font = {"align": "top"}  # Ensure edge labels are positioned correctly

    try:
        for index, row in graph_data.iterrows():
            subject = row['subject']
            predicate = row['predicate']
            object = row['object']

            if subject not in seen_nodes:
                truncated_label = subject if len(subject) < 10 else subject[:10]
                net.add_node(subject, label=truncated_label,title=subject, shape='circle')
                seen_nodes.add(subject)
            if object not in seen_nodes:
                truncated_label = object if len(object) < 10 else object[:10]
                net.add_node(object, label=truncated_label,title=object, shape='circle')
                seen_nodes.add(object)
            if subject and object and predicate:
                # Use 'label' for edge labels
                net.add_edge(subject, object, label=predicate, font={'color': 'red', 'size': 12})

        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmpfile:
            net.save_graph(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode('utf-8')

    finally:
        # Ensure the temporary file is deleted
        os.unlink(tmpfile.name)

    return html_content

        

# GETTING ALL THE NODES AND RELATIONS
nodes = [None]
nodelist = get_nodelist()
# nodes.extend(sorted(nodelist['n.name'].tolist()))
nodes.extend(nodelist['n.name'].tolist())
relations = [None]
relationlist=get_relationlist()
relations.extend(sorted(relationlist['RelationshipType'].tolist()))


graph_data = get_graph()
# print(graph_data)
# Data tabulation
all_nodes = pd.DataFrame(list(graph_data['n']) + list(graph_data['m']), columns=['node'])
node_counts = all_nodes['node'].value_counts()

# Create visualization
net = create_vis(graph_data)
path = "graph.html"
net.save_graph(path)
HtmlFile = open(path, "r", encoding='utf-8')
source_code = HtmlFile.read()


st.write("""
# ASGM DATASET
""")

# Tab selection for displaying data
tab1, tab2 = st.tabs(["Tabular", "Graphical"])

with tab1:
    st.write("Data in Tabular Format")
    # Display data in a table
    df = pd.DataFrame({
        'Subject': graph_data['n'],
        'Predicate': graph_data['r'],
        'Object': graph_data['m']
    })
    st.dataframe(df, 800, 300)

with tab2:
    st.write("Data in Graphical Format")
    # Display the saved graph
    components.html(source_code, height=900)

# Toggle button for node frequencies
if st.button('Show Node Frequencies'):
    st.session_state.show_frequencies = not st.session_state.get('show_frequencies', False)

if st.session_state.get('show_frequencies', False):
    # Display node frequencies
    all_nodes = pd.DataFrame(list(graph_data['n']) + list(graph_data['m']), columns=['node'])
    node_counts = all_nodes['node'].value_counts()
    node_frequencies_html = "<div style='height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;'>"
    for node, count in node_counts.items():
        node_frequencies_html += f"<p>{node}: {count}</p>"
    node_frequencies_html += "</div>"
    st.markdown(node_frequencies_html, unsafe_allow_html=True)

st.write("""
# Query and Answer (QnA) 
         There are four ways an user can query the knowledge graph. 
         - Select the source node and get the graph information associated with it. 
         - Select the target node and get the graph information associated with it.
         - Select any relation and get the nodes associated with it.
         - Select Source and Target nodes and get the relations associated with them.

""")

st.markdown(
    """
<span style="color: brown;">
<b>Please Always Reset to None the values of Subject, Predicate, and Object to play with above types of Query.</b>
</span>
""",
    unsafe_allow_html=True
)

st.title('Query and Answer (QnA) the Knowledge Graph')

# Using columns to align the labels and dropdowns
col1, col2, col3 = st.columns(3)

with col1:
    st.write("Subject")
    # The default value is 'None', followed by the entries in the nodelist
    subject = st.selectbox("", nodes, index=0,key='subject_select')

with col2:
    st.write("Predicate")
    # The default value is 'None', followed by the entries in the relationlist
    predicate = st.selectbox("",relations, index=0,key='predicate_select')

with col3:
    st.write("Object")
    # The default value is 'None', followed by the entries in the nodelist
    object = st.selectbox("",nodes, index=0,key='object_select')

if subject is None and predicate is None and object is None:
    st.info("Please select a subject, or a predicate or an object.")
else:
    qna_query = """
        MATCH (n)-[r]->(m)
    """
    condition = []
    if subject is not None:
        condition.append(f"n.name = '{subject}'")
    if object is not None:
        condition.append(f"m.name = '{object}'")
    if predicate is not None:
        condition.append(f"TYPE(r) = '{predicate}'")
    if condition:
        qna_query += ' WHERE ' + ' AND '.join(condition)

    qna_query += ' RETURN n.name as subject, TYPE(r) as predicate, m.name as object'
    print(f"Query Strucute: {qna_query}")
        
    qna_answer = get_QnA(qna_query)
    if len(qna_answer) !=0:
        tab1, tab2 = st.tabs(["Graph", "Dataframe"])
        with tab1:
            graph_qna = get_QnA_graph(qna_answer)
            components.html(graph_qna, height=900)
        with tab2:
            df = pd.DataFrame({
            'Subject': qna_answer['subject'],
            'Predicate': qna_answer['predicate'],
            'Object': qna_answer['object']
            })
            st.dataframe(df, 500)



        
    else:
        st.error("No Relation is found")



st.write("# SUMMARY of the Graph")

hop_col, norm_col = st.tabs(["Approach 1", "Approach 2"])



with hop_col:
    col1, col2 = st.columns(2)
    with col1:
        source_node = st.selectbox("Select Source Node", nodes, index=0, key='source_node_select')
    with col2:
        hop_list=[1,2,3]
        k_hop = st.selectbox("Input for K-hop Distance", hop_list, index=0,key='hop')
    
    summary_overall = get_hop_summary(source_node, k_hop)
  
    summary_df = pd.DataFrame(summary_overall)
    print(f"Source node :{source_node}, k_hop :{k_hop}")
    print(f"Type of source: {type(source_node)}")
    result =  create_summary(summary_df)
    if source_code is None:
        st.error("Select a Source Node")
    else:
        if st.button('Summary',key='summary1'):
            # with summary:
            print(result)
            st.write(result)
            # with dataframe:
            #     st.table(summary_df)


with norm_col:
    col1, col2 = st.columns(2)
    with col1:
        source_node = st.selectbox("Select Source Node", nodes, index=0, key='source_node_select1')
    with col2:
        dest_node = st.selectbox("Select Destination Node", nodes, index=0, key='dest_node1')
    summary_overall2 = get_hop_summary2(source_node, dest_node)
    summary_df2 = pd.DataFrame(summary_overall2)
    print(summary_df2)
    print(f"Source node :{source_node}, Dest_node :{dest_node}")
    result2 =  create_summary(summary_df2)

    if source_node is None and dest_node is None:
        st.error("Choose a Source or Destination Node")
    else:
        if st.button('Summary',key='summary2'):
            print(result2)
            st.write(result2)


st.write("# WANT to HAVE a chat with the Graph")
user_input = st.text_input('Enter your text:', max_chars=50)

if user_input!='':
    response = ask_query(user_input)
    print(f"Type text: {response}")
    print(response)
    st.write(response)