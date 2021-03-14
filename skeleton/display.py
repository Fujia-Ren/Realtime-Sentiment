

def get_data_from_db():
    """
      db means cosmos db (HASHTAG DB).
      Replace below example with 
      a query of 10 (or any) hashtags with the most counts
    """
    example = [
        {
            "tag_name": "BLM",
            "sentiment": 0.6,
            "count": 1000

        },
        {
            "tag_name": "chess",
            "sentiment": 0.3,
            "count": 1000
        }
        # ... and 8 more (to show top 10)
    ]
    return example


def update_display(data):
    """
      Below is a placeholder for the frontend. But it is suffice for now...
    """
    print(data)


if __name__ == "__main__":

    while(True):
      # For every min/hour/day (doesn't matter)
        data = get_data_from_db()
        update_display(data)
