from models.relationship_mapping import RelationshipMapping
import logging

# def generate_relationship_csv_header(relationship: RelationshipMapping):
#     result = f",{relationship.end_node.filename()}.id"
#     return result

# def generate_csv_relationship(
#     relationship: RelationshipMapping,
#     export_folder: str,
#     ):
#     # Will generate a .csv file for use with Neo4j's data-importer.

# def generate_csv_relationships(
#     relationships: dict[str, RelationshipMapping],
#     export_folder: str):
#     # Will generate .csvs and a .json file for use with Neo4j's data-importer. Returns filename of .csv file
    
#     # Generate relationships
#     for relationship in relationships:

#         logging.info(f"Generating node: {relationship}")

#         # Generate the .csv file
#         filename = f"{export_folder}/{relationship.filename()}.csv"

#         with open(filename, 'w') as f:
#             # Write the header
#             header = f":START_ID,:END_ID,:TYPE\n"
#             f.write(header)
#             # Write the rows
#             for row in relationship.rows:
#                 row = f"{row[0]},{row[1]},{row[2]}