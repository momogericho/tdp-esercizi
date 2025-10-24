from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCromosomi():
        list_cromosomi = []
        db = DBConnect()
        conn = db.get_connection()
        cursor = conn.cursor()
        query = """select distinct g.Chromosome as chromosome 
                   from genes g
                   where chromosome != 0
                   order by chromosome asc"""
        cursor.execute(query)
        for row in cursor:
            list_cromosomi.append(row["chromosome"])
        cursor.close()
        conn.close()
        return list_cromosomi

    @staticmethod
    def getAllWeightedEdges():
        list_archi_pesati = []
        db = DBConnect()
        conn = db.get_connection()
        cursor = conn.cursor()
        query = """select tb.cromosoma1 as cr1,tb.cromosoma2 as cr2,SUM(tb.exp_corr ) as weight
                   from(

                        select g1.Chromosome as cromosoma1,g2.Chromosome as cromosoma2,i.GeneID1 as gene1, i.GeneID2 as gene2, i.Expression_Corr as Exp_corr
                        from interactions as i,genes g1,genes g2
                        where g1.Chromosome != g2.Chromosome and g1.Chromosome !=0 and g2.Chromosome !=0 and g1.GeneID = i.GeneID1 and g2.GeneID = i.GeneID2) as tb
                    group by tb.cromosoma1 ,tb.cromosoma2 
                """
        cursor.execute(query)
        for row in cursor:
            list_archi_pesati.append((row["cr1"],row["cr2"],row["weight"]))
        cursor.close()
        conn.close()
        return list_archi_pesati