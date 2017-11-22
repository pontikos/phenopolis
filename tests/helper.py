from views import neo4j_driver
from views.neo4j_setup import create_demo_user
from passlib.hash import argon2


def login(app):
    return app.post('/login', data=dict(
        name='demo',
        password='demo123'
    ), follow_redirects=True)


# We won't load from csv file because Neo4j is set up by default to load only from 
# folder <neo4j-home>\import and we don't have access to change this on Travis-CI.
def load_neo4j_test_data():  
    with neo4j_driver.session() as neo4j_session:
        neo4j_session.run("CREATE (a:User {user: {username}, argon_password: {hash}})",
                    {"username": "testSuite", "hash": argon2.hash("demo123")})


def delete_neo4j_test_data():
    with neo4j_driver.session() as neo4j_session:
        neo4j_session.run("MATCH (a:User) WHERE a.user = {username} "
                    "DETACH DELETE a",
                    {"username": "testSuite"})


def create_neo4j_demo_user():  
    with neo4j_driver.session() as neo4j_session:
        create_demo_user(neo4j_session)

def my_patients_neo4j_data():
    user='demo'
    with neo4j_driver.session() as neo4j_session:



        ## genes
        #s="""
        #MERGE (g:Gene {gene_name:"TTLL5"})
        #MERGE (g1:Gene {gene_name:"DRAM2"})
        #MERGE (g2:Gene {gene_name:"RPGR"});
        #""" 
        #result = neo4j_session.run(s)

        ## person1
        #s="""
        #MATCH (u:User {user:'%s'})
        #MERGE (u)-[r:WRITES]->(p:Person {personId:"person1", gender:"M", score:0.69});
        #""" % (user)
        #result = neo4j_session.run(s)

        ## person2
        #s="""
        #MATCH (u:User {user:'%s'})
        #MERGE (u)-[r:WRITES]->(p:Person {personId:"person2", gender:"F", score:0.69})
        #""" % (user)
        #result = neo4j_session.run(s)

        ## Person to Gene
        #s="""
        #MATCH (p:Person {personId:"person1"}), (g:Gene {gene_name:"TTLL5"})
        #MERGE (p)-[:CandidateGene]->(g);
        #"""
        #result = neo4j_session.run(s)


        # person1
        s="""
        MATCH (u:User {user:'%s'})
        MERGE (u)-[r:WRITES]->(p:Person {personId:"person1", gender:"M", score:0.69})
        MERGE (t:Term {termId:"HP:0000505", name:"Visual impairment"})
        MERGE (p)-[:PersonToObservedTerm]->(t)
        MERGE (p)-[:CandidateGene]->(g:Gene {gene_name:"TTLL5"})
        MERGE (gv1:GeneticVariant {variantId:"22-38212762-A-G", allele_freq:0.0002, kaviar_AF:0.000006})
        MERGE (gv2:GeneticVariant {variantId:"14-76201609-C-G", allele_freq:0.0002, kaviar_AF:0.000006})
        MERGE (p)<-[:HomVariantToPerson]-(gv1)
        MERGE (p)<-[:HetVariantToPerson]-(gv2);
        """ % (user)
        result = neo4j_session.run(s)

        # person2
        s="""
        MATCH (u:User {user:'%s'}), (g:Gene {gene_name:"TTLL5"}), 
            (gv1:GeneticVariant {variantId:"22-38212762-A-G"}), 
            (gv2:GeneticVariant {variantId:"14-76201609-C-G"})
        MERGE (u)-[r:WRITES]->(p:Person {personId:"person2", gender:"F", score:0.69})
        MERGE (t505:Term {termId:"HP:0000505", name:"Visual impairment"})
        MERGE (t479:Term {termId:"HP:0000479", name:"Abnormality of the retina"})
        MERGE (p)-[:PersonToObservedTerm]->(t505)
        MERGE (p)-[:PersonToObservedTerm]->(t479)
        MERGE (p)-[:CandidateGene]->(g)
        MERGE (p)-[:CandidateGene]->(g1:Gene {gene_name:"DRAM2"})
        MERGE (p)-[:CandidateGene]->(g2:Gene {gene_name:"RPGR"})
        MERGE (gv3:GeneticVariant {variantId:"14-12312312-C-G", allele_freq:0.0002, kaviar_AF:0.000006})
        MERGE (p)<-[:HomVariantToPerson]-(gv1)
        MERGE (p)<-[:HetVariantToPerson]-(gv2)
        MERGE (p)<-[:HetVariantToPerson]-(gv3);
        """ % (user)
        result = neo4j_session.run(s)

        #Gene to HPO term
        s="""
        MATCH (g:Gene {gene_name:"TTLL5"}), 
            (t505:Term {termId:"HP:0000505"}), (t479:Term {termId:"HP:0000479"})
        MERGE (g)-[:GeneToTerm]->(t505)
        MERGE (g)-[:GeneToTerm]->(t479);
        """ 
        result = neo4j_session.run(s)

        #Genetic variant to transcript variant
        s="""
        MATCH (gv1:GeneticVariant {variantId:"22-38212762-A-G"})
        MERGE (gv1)-[:GeneticVariantToTranscriptVariant]->(:TranscriptVariant {variantId:"Variant 01"})
        """ 
        result = neo4j_session.run(s)
        


 

