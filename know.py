import rdflib
import ast

g = rdflib.Graph()
g.parse("南大知識庫第二季.rdf")


# 給定Triple的任兩個元素，查詢第三個
def triple(_subject="rdf:錢炳全", _predicate="?x", _object="rdf:錢炳全的研究室"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{ {} {} {}}}""".format(_subject, _predicate, _object))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
    return results


# 一個Instance下的某個Property
def property_of_instance(_subject="rdf:錢炳全", _property="rdf:專長"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{ {} {} ?x}}""".format(_subject, _property))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'])
    return results


# 一個Class下所有的Properties名稱
def properties_of_class(class_name="rdf:教授"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT distinct ?p
    WHERE {{
    ?x a {} .
    ?x ?p ?obj
    }}""".format(class_name))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['p']['value'][70:])
    return results


# 一個Class下的所有Instances
def instances_of_class(class_name="rdf:教授"):
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


def special_triple(answer_class="rdf:實驗室", relation="rdf:管理人員", entity="rdf:錢炳全"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{
    ?x a {} .
    ?x {} {}
    }}""".format(answer_class, relation, entity))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
    return results


def query(command, *args):
    if command == 1:
        answer = triple(*args)
    elif command == 2:
        answer = property_of_instance(*args)
    elif command == 3:
        answer = properties_of_class(*args)
    elif command == 4:
        answer = instances_of_class(*args)
    elif command == 5:
        answer = special_triple(*args)
    else:
        answer = "bye"

    if not answer:
        return "沒有答案"
    else:
        return " ".join(answer)
