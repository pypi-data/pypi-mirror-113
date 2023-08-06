from bergen.query import DelayedGQL





CREATE_SAMPLE = DelayedGQL("""
mutation SampleCreate($name: String, $creator: String) {
  createSample(name: $name, creator: $creator){
    id
    name
    creator {
        email
    }
  }
}
""")