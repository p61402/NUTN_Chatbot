import rdflib
import ast

dir_path = "知識庫/"
g = rdflib.Graph()
g.parse(dir_path + "南大知識庫第三季.rdf")


# 給定Triple的任兩個元素，查詢第三個
def triple(_subject="rdf:錢炳全", _predicate="rdf:開課", condition01="", condition02="", condition03="", _object="?x"):
    if condition01 and condition02 and condition03:
        print("IRCPPv")
        results = IRCPPv(condition01, _predicate, _subject, condition02, condition03)
    elif condition01 and condition02:
        print("IRPPv")
        results = IRPPv(_subject, _predicate, condition01, condition02)
    elif condition01:
        print("IRC")
        results = IRC(condition01, _predicate, _subject)
    else:
        r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
        SELECT ?x
        WHERE {{ {} {} {} }}""".format(_subject, _predicate, _object))

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


# 一個Class下(滿足一個property)的所有Instances
def instances_of_class(class_name="rdf:教授", _property="", string=""):
    if _property:
        r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
        SELECT ?x
        WHERE {{
        ?x a {} .
        ?x {} ?y
        FILTER(REGEX(str(?y), "{}"))
        }}""".format(class_name, _property, string))
    else:
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


# 一個Instance所屬的Class
def class_of_instance(instance_name="rdf:錢炳全"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
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


# 一個Class底下的所有Subclass
def subclasses_of_class(class_name="rdf:課程"):
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


# 某個Class下滿足一個Property的instance個數
def count_instances_of_class(class_name="rdf:課程", _property="", string=""):
    if _property:
        r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
        SELECT (COUNT(?x) AS ?COUNT)
        WHERE {
        ?x a {} .
        ?x {} ?y
        FILTER(REGEX(str(?y), "{}"))
        }""".format(class_name, _property, string))
    else:
        r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
        SELECT (COUNT(?x) AS ?COUNT)
        WHERE {{
        ?x a {}
        }}""".format(class_name))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['COUNT']['value'])
    return results


# 在某個Class下的一個Triple
def IRC(class_name="rdf:大三課程", _relation="rdf:授課老師", _object="rdf:錢炳全"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{
    ?x a {} .
    ?x {} {}
    }}""".format(class_name, _relation, _object))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
    return results


# 滿足某個Property的一個Triple
def IRPPv(_subject="rdf:錢炳全", _relation="rdf:開課", _property="rdf:修別", string="選修"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{
    {} {} ?x .
    ?x {} ?y .
    FILTER(REGEX(str(?y), "{}"))
    }}""".format(_subject, _relation, _property, string))

    data = ast.literal_eval(r.serialize(format="json").decode("utf8"))
    results = []
    for i in range(len(data['results']['bindings'])):
        results.append(data['results']['bindings'][i]['x']['value'][70:])
    return results


# 在某個Class下滿足某個Property條件的一個Triple
def IRCPPv(class_name="rdf:大三課程", _relation="rdf:授課老師", _object="rdf:錢炳全", _property="rdf:修別", string="選修"):
    r = g.query("""PREFIX rdf: <http://www.semanticweb.org/user/ontologies/2017/6/untitled-ontology-8#>
    SELECT ?x
    WHERE {{
    ?x a {} .
    ?x {} {} .
    ?x {} ?y .
    FILTER(REGEX(str(?y), "{}"))
    }}""".format(class_name, _relation, _object, _property, string))

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
        answer = class_of_instance(*args)
    elif command == 6:
        answer = subclasses_of_class(*args)
    elif command == 7:
        answer = count_instances_of_class(*args)
    else:
        answer = ""

    return "、".join(answer)
