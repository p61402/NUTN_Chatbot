import rdflib
import ast

dir_path = "知識庫/"
g = rdflib.Graph()
g.parse(dir_path + "南大知識庫第三季.rdf")


def invalid_query():
    return []


# 一個Class底下的所有Subclass
def class_subclass(class_name="rdf:課程"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?subClass
    WHERE {{
    ?subClass rdfs:subClassOf {} .
    }}""".format(class_name))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['subClass']['value'][70:])
    return results


# 一個Class下(滿足一個property)的所有Instances
def class_instance(class_name="rdf:資工系教授"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{
    ?x a {} .
    }}""".format(class_name))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
    return results


# 一個Class的所有Relation
def class_relation(_subject="rdf:實驗室"):
    r = g.query("""
    PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?domain ?property ?range
    WHERE {{
    ?property rdfs:domain ?domain ;
              rdfs:range ?range .
    {} (rdfs:domain/rdfs:range)* ?domain .
    }}""".format(_subject))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['property']['value'][70:])
    return list(set(results))


def instance_all_properties(instance="rdf:勝利早點"):
    r = g.query("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?p ?v
    WHERE{{
    ?p a owl:DatatypeProperty .
    {} ?p ?v .
    }}""".format(instance))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append((data['results']['bindings'][i]['p']['value'][70:], data['results']['bindings'][i]['v']['value']))
    return results


# 一個Instance所屬的Class
def instance_superclass(instance_name="rdf:錢炳全"):
    r = g.query("""
    PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?class
    WHERE {{
    {} a ?class .
    }}""".format(instance_name))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        ans = data['results']['bindings'][i]['class']['value'][70:]
        if ans:
            results.append(ans)
    return results


def instance_relation(_subject="rdf:離散數學"):
    r1 = g.query("""
    PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?p
    WHERE {{
    {} ?p ?o
    }}""".format(_subject))

    r2 = g.query("""
    PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?p
    WHERE {{
    ?o ?p {}
    }}""".format(_subject))

    data1 = ast.literal_eval(r1.serialize(format="json").decode("utf8"))
    data2 = ast.literal_eval(r2.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data1['results']['bindings'])):
        ans = data1['results']['bindings'][i]['p']['value'][70:]
        if ans:
            results.append(ans)
    for i in range(len(data2['results']['bindings'])):
        ans = data2['results']['bindings'][i]['p']['value'][70:]
        if ans:
            results.append(ans)
    return results


def class_relation_class(_class="rdf:資工系課程", relation="rdf:授課老師"):
    r = g.query("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT DISTINCT ?x
    WHERE{{
    {} rdfs:domain {} .
    {} rdfs:range ?x .
    }}""".format(relation, _class, relation))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
    return results


def class_class_relation(_class1="rdf:實驗室", _class2="rdf:行政人員"):
    r = g.query("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT DISTINCT ?x ?y
    WHERE{{
    ?x rdfs:domain {} .
    ?x rdfs:range {} .
    ?y rdfs:range {} .
    ?y rdfs:domain {}
    }}""".format(_class1, _class2, _class1, _class2))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
        results.append(data['results']['bindings'][i]['y']['value'][70:])
    return results


# Triple求instance
def instance_relation_instance(instance1="rdf:錢炳全", relation="rdf:開課"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{ {} {} ?x }}""".format(instance1, relation))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
    return results


# Triple求relation
def instance_instance_relation(instance1="rdf:錢炳全", instance2="rdf:資料庫與資訊知識系統實驗室"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{ {} ?x {} }}""".format(instance1, instance2))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
    return results


# 一個Instance下的某個Property
def instance_property_propertyValue(instance="rdf:錢炳全", _property="rdf:專長"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{ {} {} ?x}}""".format(instance, _property))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'])
    return results


# 所有class2的instance滿足class1-relation-class2
def class_relation_class_instance(class1="rdf:大三課程", relation="rdf:授課老師", class2="rdf:資工系教授"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{
    ?x a {} .
    ?y a {} .
    ?x {} ?y
    }}""".format(class1, class2, relation, class2))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
    return results


# 一個Class下滿足某個property的所有instance
def class_property_propertyValue_instance(_class="rdf:大二課程", property_name="rdf:修別", propertyValue="必修"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{
    ?x a {} .
    ?x {} ?y .
    FILTER(REGEX(str(?y), "{}"))
    }}""".format(_class, property_name, propertyValue))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
    return results


def class_relation_instance_instance(_class="rdf:大三課程", relation="rdf:授課老師", instance="rdf:錢炳全"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{
    ?x a {} .
    ?x {} {}
    }}""".format(_class, relation, instance))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
    return results


# 滿足某個property的triple
def instance_relation_property_propertyValue_instance(instance="rdf:李建樹", relation="rdf:開課", property_name="rdf:修別", properyValue="選修"):
    r = g.query("""
    PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{
    {} {} ?x .
    ?x {} ?y .
    FILTER(REGEX(str(?y), "{}"))
    }}""".format(instance, relation, property_name, properyValue))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
    return results


def class_property_propertyValue_relation_class_instance(_class="rdf:大三課程", _property="rdf:修別", propertyValue="選修", relation="rdf:授課老師"):
    r = g.query("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT DISTINCT ?z
    WHERE {{
    ?x a {} .
    ?x {} ?y .
    FILTER(REGEX(str(?y), "{}"))
    ?x {} ?z
    }}""".format(_class, _property, propertyValue, relation))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['z']['value'][70:])
    return results


def class_relation_class_instance_property_propertyValue(_class="rdf:大三課程", relation="rdf:授課老師", _property="rdf:專長", propertyValue="機器學習"):
    r = g.query("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT DISTINCT ?y
    WHERE {{
    ?x a {} .
    ?x {} ?y .
    ?y {} ?z
    FILTER(REGEX(str(?z), "{}"))
    }}""".format(_class, relation, _property, propertyValue))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['y']['value'][70:])
    return results


query_functions = {-1: invalid_query,
                   0: class_instance,
                   1: instance_superclass,
                   2: class_relation_class,
                   3: class_class_relation,
                   4: instance_relation_instance,
                   5: instance_instance_relation,
                   6: instance_property_propertyValue,
                   7: class_relation_class_instance,
                   8: class_property_propertyValue_instance,
                   9: class_relation_instance_instance,
                   10: instance_relation_property_propertyValue_instance,
                   11: class_property_propertyValue_relation_class_instance,
                   12: class_relation_class_instance_property_propertyValue,
                   13: instance_relation,
                   14: class_relation,
                   15: class_subclass,
                   16: instance_all_properties}


def make_query(query_number, *args):
    response = query_functions[query_number](*args)
    return response


# print(class_subclass())
# print(class_instance())
# print(class_relation())
# print(instance_superclass())
# print(instance_relation())
# print(class_relation_class())
# print(class_class_relation())
# print(instance_relation_instance())
# print(instance_instance_relation())
# print(instance_property_propertyValue("rdf:錢炳全", "rdf:專長"))
# print(class_relation_class_instance())
# print(class_property_propertyValue_instance())
# print(class_relation_instance_instance())
# print(instance_relation_property_propertyValue_instance())
# print(class_property_propertyValue_relation_class_instance())
# print(class_relation_class_instance_property_propertyValue())
