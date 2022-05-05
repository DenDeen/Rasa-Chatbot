import json

from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask
from flask_restful import Resource, Api
from vocabulary.vocabulary import Vocabulary as vb

from nlp import find_entities


def obtain_result(named_entity, query_properties):
    property_code = []

    if len(query_properties) != 0:
        properties = open('property.json', 'r')
        properties = json.load(properties)
        print(type(properties))

        noun = query_properties[0]

        noun_synonyms = vb.synonym(noun, format="dict")

        for p, prop in properties.items():
            if prop == noun:
                property_code.append(p)
                break

        if len(property_code) == 0:
            for p, prop in properties.items():
                if type(noun_synonyms) != bool:
                    for synonym in noun_synonyms.itervalues():
                        if prop == synonym:
                            property_code.append(p)
                            break

        print(property_code)

    if len(named_entity) != 0:
        if len(property_code) != 0:
            flag = 0
            sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
            query = """SELECT ?label ?property ?thumbnail WHERE
                        { 
                        ?entity rdfs:label ?label .
                        ?entity wdt:""" + property_code[0] + """ ?property_id .
                        ?property_id rdfs:label ?property .
                        OPTIONAL { ?property_id wdt:P18 ?thumbnail .}
                        FILTER (STR(?label) = '""" + named_entity[0] + """') .
                        FILTER (LANG(?property) = "en")
                        }"""
            print(query)
        else:
            flag = 1
            sparql = SPARQLWrapper("https://dbpedia.org/sparql")
            query = """SELECT ?label ?description ?thumbnail WHERE
                { 
                ?entity rdfs:label ?label .
                ?entity dbo:abstract ?description .
                ?entity dbo:thumbnail ?thumbnail .
                FILTER (STR(?label) = '""" + named_entity[0] + """' && LANG(?description) = "en") .
                }
                LIMIT 1"""
            print(query)

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        global result
        result = list()
        temp = str()
        try:
            results = sparql.query().convert()
            print(results)

            if flag == 0:
                for data in results["results"]["bindings"]:
                    result.append(data["property"]["value"])

                    if "thumbnail" in data and data["thumbnail"]["value"] != "":
                        temp = data["thumbnail"]["value"]
            else:
                for data in results["results"]["bindings"]:
                    result.append(data["description"]["value"])

                    if "thumbnail" in data and data["thumbnail"]["value"] != "":
                        temp = data["thumbnail"]["value"]

            result = list(set(result))
            response = []
            for i in result:
                print(i)
                response.append(u''.join(i).encode('utf-8'))
            print(response)

            if flag == 0:
                data = {"status": "200", "data": response, "thumbnail": temp}
            else:
                data = {"status": "200", "data": response, "thumbnail": temp}
            result = json.dumps(data)
            print(results)
        except:
            response = ["Unable to retrieve data"]
            data = {"status": "500", "data": response}
            result = json.dumps(data)
            raise
    else:
        response = ["Unable to retrieve data"]
        data = {"status": "500", "data": response}
        result = json.dumps(data)

    print(result)
    return result

app = Flask(__name__)
api = Api(app)


class Query(Resource):
    def get(self, query):
        print(query)
        named_entity, query_properties = find_entities(query)
        response = obtain_result(named_entity, query_properties)
        return response


api.add_resource(Query, '/wiki/<string:query>')

if __name__ == '__main__':
    app.run()
