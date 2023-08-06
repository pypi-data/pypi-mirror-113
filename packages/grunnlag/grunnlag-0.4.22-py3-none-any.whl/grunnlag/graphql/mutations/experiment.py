from bergen.query import DelayedGQL





CREATE_EXPERIMENT = DelayedGQL("""
mutation CreateExperiment($name: String!, $creator: String, $meta: GenericScalar, $description: String) {
  createExperiment(name: $name, creator: $creator, description: $description, meta: $meta){
    id
    name
    creator {
        email
    }
    meta
  }
}
""")