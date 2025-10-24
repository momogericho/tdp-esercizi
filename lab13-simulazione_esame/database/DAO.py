from database.DB_connect import DBConnect

class DAO:
    def __init__(self):
        pass

    def fillYears(self):
        list_years=[]
        db = DBConnect()
        conn= db.get_connection()
        cursor = conn.cursor()
        query= """select distinct year(s.datetime) as dateyear
                  from sighting s
                  order by dateyear desc"""
        cursor.execute(query)
        for row in cursor:
            list_years.append(row["dateyear"])
        cursor.close()
        conn.close()
        return list_years

    def fillShapes(self,year):
        list_shapes=[]
        db = DBConnect()
        conn= db.get_connection()
        cursor = conn.cursor()
        query="""select distinct s.shape as shape
                 from sighting s
                 where year(datetime) = %s 
              """
        cursor.execute(query,(year,))
        for row in cursor:
            list_shapes.append(row["shape"])
        cursor.close()
        conn.close()
        return list_shapes

    def getNodes(self):
        list_nodes = []
        db = DBConnect()
        conn = db.get_connection()
        cursor = conn.cursor()
        query = """select  st.id as id,st.Name as name,st.Capital as capital, st.Lat as lat, st.Lng as lng,st.Area as area,st.Population as population,st.Neighbors as neighbors
                   from state st
              """
        cursor.execute(query)
        for row in cursor:
            list_nodes.append(**row)
        cursor.close()
        conn.close()
        return list_nodes

    def getWeightedEdges(self,shape,year,idMapStates):
        list_edges = []
        db = DBConnect()
        conn = db.get_connection()
        cursor = conn.cursor()
        query="""select st1.id as state1,st2.id as state2,count(*) as weight
                 from state as st1,state as st2, sightings as s
                 where s.shape=%s and year(s.datetime) = %s and (st1.id == s.state or st2.id ==s.state) and st1.id in st2.neighbours and st1.id<st2.id"""
        cursor.execute(query,(shape,year,))
        for row in cursor:
            list_edges.append(idMapStates[row["state1"]],idMapStates[row["state2"]],row["weight"])
        cursor.close()
        conn.close()
        return list_edges