from django.utils.translation import gettext_lazy as _

TRANSLATIONS = {
    "global": {
        "projectTitle": _("This was Paris in 1970"),
        "labName": _("MIT Digital Humanities Lab"),
        "mapSquare": _("Map Square")
    },
    # "HomePage": {    
    "HomePage": {
        "wipModal": {
            "title": _("Pardon Our Dust!"),
            "description1": _("""
                <strong>This was Paris in 1970</strong> is a project by
                the <link1>MIT Digital Humanities Lab</link1> in collaboration with
                <link2>Catherine Clark</link2>, Associate Professor of History and French Studies
                at MIT and Director of MIT Digital Humanities.
            """),
            "description2": _("""
                This project is still under construction and contains
                student work, so there may be features that are
                currently incomplete or inaccurate.
            """),
            "close": _("Close")
        },
        "scrollDown": _("Scroll down to enter"),
        "explore": _("Explore Photos by Subject"),
        "view": _("View Photos by Location"),
        "context": _("Context and Research"),
        "about": _("About the Project")
    },
    "About": {
        "context1": _("In May 1970, thousands of amateur photographers spread out across Paris to take pictures. They were participants in a photo contest, “This was Paris in 1970,” organized by the cooperative electronics store the Fnac. Each contestant had been assigned to document a 250m square of the city. By the end of the month, this army of photographers had produced an unprecedented collection of 100,000 photographs: 70,000 black-and-white prints and 30,000 colors slides. This website currently hosts 5,000 color slides from the 13th and 19th arrondissements, areas of the city which were undergoing significant change in 1960s and 1970s."),
        "context2": _(" The project This was Paris in 1970 provides tools to explore the rich archive: a <link1>map</link1> to see the photos square by square; an <link2>object detector</link2> to search for photos of many objects from people to cats, cars to strollers; a similar photo viewer to identify photos by composition rather than subject; and <link3>articles</link3> providing context and analysis."),
        "team1": _("This is Paris in 1970 was created in MIT’s Digital Humanities Lab as a collaboration between DH Fellow <link1>Prof. Catherine Clark</link1>, <link2>four dozen undergraduate research associates</link2>, and <link3>the instructional staff</link3> of the DH Lab. Justice Vidal built out the first version of the site, and Nina Li spearheaded the design work."),
        "team2": _("The <link1>Bibliothèque historique de la Ville de Paris</link1> holds the contest photographs. Its photo department made this project possible."),
    },
    "Explore": {
        "rangeError": _('Desired page out of range'),
        "paginationText1": _("Page {{currentPage}} of {{totalPages}}"),
        "paginationText2": _("Showing Photos {{startImage}} - {{endImage}} out of {{totalCount}}"),
        "previous": _("Previous Page"),
        "goTo": _("Go to Page: "),
        "next": _("Next Page"),
        "go": _("Go"),
        "objectsLabel": _("Objects"),
        "objectDropdownDefault": _("All"),
        "objectTags": {
            "person": _("person"),
            "bicycle": _("bicycle"),
            "car": _("car"),
            "motorbike": _("motorbike"),
            "aeroplane": _("aeroplane"),
            "bus": _("bus"),
            "train": _("train"),
            "truck": _("truck"),
            "boat": _("boat"),
            "traffic light": _("traffic light"),
            "fire hydrant": _("fire hydrant"),
            "stop sign": _("stop sign"),
            "parking meter": _("parking meter"),
            "bench": _("bench"),
            "bird": _("bird"),
            "cat": _("cat"),
            "dog": _("dog"),
            "horse": _("horse"),
            "sheep": _("sheep"),
            "cow": _("cow"),
            "elephant": _("elephant"),
            "bear": _("bear"),
            "zebra": _("zebra"),
            "giraffe": _("giraffe"),
            "backpack": _("backpack"),
            "umbrella": _("umbrella"),
            "handbag": _("handbag"),
            "tie": _("tie"),
            "suitcase": _("suitcase"),
            "frisbee": _("frisbee"),
            "skis": _("skis"),
            "snowboard": _("snowboard"),
            "sports ball": _("sports ball"),
            "kite": _("kite"),
            "baseball bat": _("baseball bat"),
            "baseball glove": _("baseball glove"),
            "skateboard": _("skateboard"),
            "surfboard": _("surfboard"),
            "tennis racket": _("tennis racket"),
            "bottle": _("bottle"),
            "wine glass": _("wine glass"),
            "cup": _("cup"),
            "fork": _("fork"),
            "knife": _("knife"),
            "spoon": _("spoon"),
            "bowl": _("bowl"),
            "banana": _("banana"),
            "apple": _("apple"),
            "sandwich": _("sandwich"),
            "orange": _("orange"),
            "broccoli": _("broccoli"),
            "carrot": _("carrot"),
            "hot dog": _("hot dog"),
            "pizza": _("pizza"),
            "donut": _("donut"),
            "cake": _("cake"),
            "chair": _("chair"),
            "sofa": _("sofa"),
            "pottedplant": _("pottedplant"),
            "bed": _("bed"),
            "diningtable": _("diningtable"),
            "toilet": _("toilet"),
            "tvmonitor": _("tvmonitor"),
            "laptop": _("laptop"),
            "mouse": _("mouse"),
            "remote": _("remote"),
            "keyboard": _("keyboard"),
            "cell phone": _("cell phone"),
            "microwave": _("microwave"),
            "oven": _("oven"),
            "toaster": _("toaster"),
            "sink": _("sink"),
            "refrigerator": _("refrigerator"),
            "book": _("book"),
            "clock": _("clock"),
            "vase": _("vase"),
            "scissors": _("scissors"),
            "teddy bear": _("teddy bear"),
            "hair drier": _("hair drier"),
            "toothbrush": _("toothbrush")
        },
        "imagePerPageLabel": _("Images per Page"),
        "toolExplanation": _("""
            Use these tools to sort photos according to subject. The object detection tool uses
            the <link1>YOLO (You Only Look Once)</link1> system. Click on any photo to view it and its metadata,
            where you will also find a gateway to the similarity algorithm.
        """),
    },
    "MapPage": {        
        "photos": _("photos"),
        "legend": {
            "arrondissment": _("Arrondissement"),
            "photosAvailable": _("Photos available"),
        },
        "return": _("Return"),
        "description": _("""
            In order to document the entire city, and not just its most touristy or photogenic neighborhoods,
            the organizers of “This was Paris in 1970” divided up the city in 1755 squares and assigned
            participants to document a square. Each square measured 250m by 250m. Because there were
            more participants than squares, many contain documentation by multiple people. Squares that
            contain no photos here were likely captured in black-and-white prints, which are available at the
            BHVP in Paris.
        """),
        "instructions": _("Click on a square to see photos taken there."),
    },
    "MapSquare": {
        "notInDB": _("Map Square {{squareNum}} is not in the database."),
        "noMetadata": _("No metadata has been transcribed for these photos."),
    },
    "PhotographerSearch": {},
    "Photographer": {
        "notInDB": _("Photographer number {{photographerNum}} is not in the database."),
        "profile": _("Photographer Profile"),
        "number": _("Number"),
        "sex": _("Recorded Sex"),
        "address": _("Address"),
        "noRecord": _("No Record"),
        "photosTaken": _("{{name}} took a total of {{numPhotos}} photos for the competition."),
        "activity": _("MAP OF ACTIVITY"),
    },
    # },
    "description": _("This project is still under construction and contains student work, so there may be features that are currently incomplete or inaccurate.")
}