import graphform

def main():

    pairs  = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
            (0,8),(0,9),(0,10),(0,11),(0,12),
            (0,13),(0,14),(0,15),(0,16),(0,17),(0,18),
            (0,19),(0,20),(0,21),(0,22),
            (1,2),(2,3),(3,1),
            (1,4),(2,4),(2,5),(3,5),(3,6),(1,6),
            (1,7),(4,7),(2,8),(5,8),(3,9),(6,9),
            (2,10),(4,10),(3,11),(5,11),(1,12),(6,12),
            (4,13),(7,13),(5,14),(8,14),(6,15),(9,15),
            (4,16),(10,16),(5,17),(11,17),(6,18),(12,18),
            (10,19),(16,19),(11,20),(17,20),(12,21),(18,21),
            (18,22),(21,22),]

    graphform.Render(pairs)


if __name__ == "__main__":
    main()