from bergen.query import DelayedGQL


CREATE_REPRESENTATION = DelayedGQL("""
mutation Representation($sample: ID, $name: String, $tags: [String], $variety: RepresentationVarietyInput, $creator: String){
  createRepresentation(sample: $sample, name: $name, tags: $tags, variety: $variety, creator: $creator){
    name
    id
    variety
    tags
    store
    unique
  
  }
}
""")

UPDATE_REPRESENTATION = DelayedGQL("""
mutation Representation($id: ID!){
  updateRepresentation(rep: $id){
    name
    id
    variety
    tags
    store
    unique
  }
}
""")