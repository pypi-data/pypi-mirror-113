from bergen.query import DelayedGQL


CREATE_REPRESENTATION = DelayedGQL("""
mutation Representation($sample: ID, $name: String, $tags: [String], $variety: RepresentationVarietyInput, $creator: String, $meta: GenericScalar){
  createRepresentation(sample: $sample, name: $name, tags: $tags, variety: $variety, creator: $creator, meta: $meta){
    name
    id
    variety
    tags
    store
    unique
    meta
  
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
    meta
  }
}
""")