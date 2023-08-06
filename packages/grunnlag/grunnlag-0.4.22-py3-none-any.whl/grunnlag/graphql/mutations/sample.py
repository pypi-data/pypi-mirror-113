from bergen.query import DelayedGQL





CREATE_SAMPLE = DelayedGQL("""
mutation SampleCreate($name: String, $creator: String, $meta: GenericScalar, $experiments: [ID]) {
  createSample(name: $name, creator: $creator, meta: $meta, experiments: $experiments){
    id
    name
    creator {
        email
    }
  }
}
""")