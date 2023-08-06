

from bergen.query import DelayedGQL


GET_SAMPLE = DelayedGQL("""
query Sample($id: ID!){
  sample(id: $id){
    id
    name
    meta
    experiments {
      id
    }
  }
}
""")


FILTER_SAMPLE = DelayedGQL("""
query Samples($creator: ID) {
  samples(creator: $creator) {
    name
    id
    representations {
        id
    }
    meta
    experiments {
      id
    }
  }
}
""")