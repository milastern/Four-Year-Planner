import numpy as np
import os


majors_dict = {
    "psychology": {
        "requirements": [
            {"type": "all_of", "courses": ["PSYC 201", "PSYC 202", "PSYC 301", "PSYC 302"]},
            {"type": "choose_n", "n": 2, "groups": [
                {"type": "any_of", "courses": ["PSYC 310", "PSYC 312", "PSYC 314", "PSYC 318"]},
                {"type": "any_of", "courses": ["PSYC 311", "PSYC 313", "PSYC 315", "PSYC 317"]}
            ]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["PSYC 350", "PSYC 351", "PSYC 352", "PSYC 353", "PSYC 354", "PSYC 355", "PSYC 356", "PSYC 358", "PSYC 360", "PSYC 362", "PSYC 370", "PSYC 402", "PSYC 404", "PSYC 406"]},
                {"type": "any_of", "courses": ["PSYC 440", "PSYC 441", "PSYC 442", "PSYC 443", "PSYC 445", "PSYC 447", "PSYC 450", "PSYC 451", "PSYC 452", "PSYC 453", "PSYC 454", "PSYC 455", "PSYC 456", "PSYC 457", "PSYC 470", "PSYC 490", "PSYC 491", "PSYC 498"]},
                {"type": "any_of", "courses": ["PSYC 410", "PSYC 411", "PSYC 412", "PSYC 413", "PSYC 414", "PSYC 415", "PSYC 417", "PSYC 418", "PSYC 422"]}
            ]}
        ]
    },
    "biology": {
        "requirements": [
            {"type": "all_of", "courses": ["CHEM 103", "CHEM 103L", "CHEM 206", "CHEM 206L", "BIOL 203L", "BIOL 204L", "BIOL 203", "BIOL 204"]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["MATH 131", "MATH 111", "MATH 108"]},
                {"type": "any_of", "courses": ["MATH 132", "MATH 112", "BIOL 327", "BIOL 325"]},
                {"type": "any_of", "courses": ["BIOL 302", "BIOL 304", "BIOL 306"]},
                {"type": "any_of", "courses": ["BIOL 310", "BIOL 420", "BIOL 433", "BIOL 442"]},
                {"type": "any_of", "courses": ["BIOL 311", "BIOL 312", "BIOL 318", "BIOL 410", "BIOL 412", "BIOL 417", "BIOL 426", "BIOL 427"]},
                {"type": "any_of", "courses": ["BIOL 406", "BIOL 407", "BIOL 408", "BIOL 409L", "BIOL 411", "BIOL 412", "BIOL 413L", "BIOL 416", "BIOL 417", "BIOL 419", "BIOL 421", "BIOL 422", "BIOL 426", "BIOL 427", "BIOL 428", "BIOL 429", "BIOL 432", "BIOL 434", "BIOL 435",
                                               "BIOL 438", "BIOL 441", "BIOL 441", "BIOL 443", "BIOL 447", "BIOL 451", "BIOL 453L", "BIOL 456L", "BIOL 457", "BIOL 458"]},
                {"type": "any_of", "courses": ["BIOL 418", "BIOL 460"]}
            ]}
        ]
    },
    "government": {
        "requirements": [
            {"type": "all_of", "courses": ["GOVT 201", "GOVT 203", "GOVT 204", "GOVT 301"]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["GOVT 202", "GOVT 305", "GOVT 392"]},
                {"type": "any_of", "courses": ["GOVT 401", "GOVT 402", "GOVT 403", "GOVT 404", "GOVT 433", "GOVT 435", "GOVT 440", "GOVT 454", "GOVT 455", "GOVT 465", "GOVT 470", "GOVT 482", "GOVT 489", "GOVT 491", "GOVT 493", "GOVT 494", "GOVT 495", "GOVT 496", "GOVT 498"]}
            ]},
            {"type": "choose_n", "n": 5, "groups": [
                {"type": "any_of", "courses": ["GOVT 150", "GOVT 302", "GOVT 305", "GOVT 306", "GOVT 307", "GOVT 310", "GOVT 311", "GOVT 312", "GOVT 322", "GOVT 324", "GOVT 235", "GOVT 326", "GOVT 327", "GOVT 328", "GOVT 329", "GOVT 330", "GOVT 334", "GOVT 335",
                                               "GOVT 336", "GOVT 337", "GOVT 338", "GOVT 339", "GOVT 340", "GOVT 350", "GOVT 351", "GOVT 352", "GOVT 353", "GOVT 355", "GOVT 360", "GOVT 361", "GOVT 370", "GOVT 372", "GOVT 373", "GOVT 374", "GOVT 388", "GOVT 389", "GOVT 390",
                                               "GOVT 391", "GOVT 392", "GOVT 393", "GOVT 394", "GOVT 401", "GOVT 402", "GOVT 403", "GOVT 404", "GOVT 433", "GOVT 435", "GOVT 440", "GOVT 454", "GOVT 455", "GOVT 465", "GOVT 470", "GOVT 482", "GOVT 489", "GOVT 491", "GOVT 493",
                                               "GOVT 494", "GOVT 495", "GOVT 496", "GOVT 498"]}
            ]}
        ]
    },
    "economics": {
        "requirements": [
            {"type": "all_of", "courses": ["ECON 101", "ECON 102", "ECON 303", "ECON 304", "ECON 307", "ECON 308", "MATH 111"]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["ECON 341", "ECON 342", "ECON 380", "ECON 385", "ECON 400", "ECON 409", "ECON 411", "ECON 412", "ECON 413", "ECON 414", "ECON 416", "ECON 424", "ECON 425", "ECON 430", "ECON 446", "ECON 448", "ECON 449", "ECON 451", "ECON 452",
                                               "ECON 453", "ECON 456", "ECON 458", "ECON 460", "ECON 463", "ECON 465", "ECON 472", "ECON 474", "ECON 478", "ECON 484", "ECON 490", "ECON 495", "ECON 496"]}
            ]},
            {"type": "choose_n", "n": 3, "groups": [
                {"type": "any_of", "courses": ["ECON 300", "ECON 311", "ECON 315", "ECON 318", "ECON 321", "ECON 322", "ECON 323", "ECON 324", "ECON 325", "ECON 327", "ECON 331", "ECON 341", "ECON 342", "ECON 344", "ECON 346", "ECON 362", "ECON 380", "ECON 382", "ECON 384",
                                               "ECON 385", "ECON 398"]},
                {"type": "any_of", "courses": ["ECON 400", "ECON 403", "ECON 407", "ECON 408", "ECON 409", "ECON 410", "ECON 411", "ECON 412", "ECON 413", "ECON 414", "ECON 415", "ECON 416", "ECON 420", "ECON 422", "ECON 424", "ECON 425", "ECON 430", "ECON 435", "ECON 446",
                                               "ECON 448", "ECON 449", "ECON 451", "ECON 452", "ECON 453", "ECON 455", "ECON 456", "ECON 458", "ECON 460", "ECON 461", "ECON 463", "ECON 465", "ECON 472", "ECON 474", "ECON 475", "ECON 476", "ECON 478", "ECON 481", "ECON 483",
                                               "ECON 484", "ECON 485", "ECON 490", "ECON 495", "ECON 496"]}
            ]}
        ]
    },
    "computer science": {
        "requirements": [
            {"type": "all_of", "courses": ["CSCI 141", "CSCI 241", "CSCI 243", "CSCI 301", "CSCI 303", "CSCI 304", "CSCI 312", "CSCI 423", "MATH 111", "MATH 112", "MATH 211"]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["MATH 214", "CSCI 243"]},
                {"type": "any_of", "courses": ["MATH 413", "MATH 414"]}
            ]},
            {"type": "choose_n", "n": 3, "groups": [
                {"type": "any_of", "courses": ["CSCI 415", "CSCI 416", "CSCI 417", "CSCI 420", "CSCI 421", "CSCI 424", "CSCI 425", "CSCI 426", "CSCI 427", "CSCI 432", "CSCI 434", "CSCI 435", "CSCI 436", "CSCI 437", "CSCI 442", "CSCI 444", "CSCI 445", "CSCI 446", "CSCI 454",
                                               "CSCI 464", "CSCI 495", "CSCI 496"]}
            ]}
        ]
    },

    "history": {
        "requirements" : [
            {"type": "all_of", "courses": ["HIST 301"]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["HIST 490C", "HIST 491C"]},
                {"type": "any_of", "courses": ["HIST 141", "HIST 142", "HIST 161", "HIST 223", "HIST 331", "HIST 332", "HIST 333", "HIST 334", "HIST 377", "HIST 378", "HIST 379"]},
                {"type": "any_of", "courses": ["HIST 171", "HIST 172", "HIST 181", "HIST 278", "HIST 279", "HIST 280", "HIST 281", "HIST 282", "HIST 283", "HIST 284", "HIST 317", "HIST 320", "HIST 325", "HIST 327", "HIST 330", "HIST 336", "HIST 420", "HIST 478", "HIST 479"]},
                {"type": "any_of", "courses": ["HIST 111", "HIST 112", "HIST 240", "HIST 241", "HIST 242", "HIST 243", "HIST 260", "HIST 261", "HIST 336", "HIST 357", "HIST 358", "HIST 359", "HIST 360", "HIST 361", "HIST 362", "HIST 363", "HIST 364", "HIST 367", "HIST 368",
                                                "HIST 369", "HIST 370", "HIST 373", "HIST 377", "HIST 378", "HIST 379", "HIST 382", "HIST 383", "HIST 384", "HIST 385", "HIST 386", "HIST 387", "HIST 388", "HIST 391", "HIST 392"]},
                {"type": "any_of", "courses": ["HIST 131", "HIST 132", "HIST 304", "HIST 306", "HIST 309", "HIST 344"]},
                {"type": "any_of", "courses": ["HIST 121", "HIST 122", "HIST 213", "HIST 214", "HIST 215", "HIST 216", "HIST 217", "HIST 218", "HIST 219", "HIST 220", "HIST 221", "HIST 222", "HIST 223", "HIST 224", "HIST 226", "HIST 228", "HIST 230", "HIST 235", "HIST 236",
                                                "HIST 237", "HIST 238", "HIST 255", "HIST 256", "HIST 315", "HIST 318", "HIST 319", "HIST 320", "HIST 321", "HIST 327", "HIST 330", "HIST 341", "HIST 342", "HIST 344", "HIST 345", "HIST 346", "HIST 347", "HIST 348", "HIST 350",
                                                "HIST 351", "HIST 352", "HIST 353", "HIST 355", "HIST 362", "HIST 393", "HIST 394", "HIST 400", "HIST 401", "HIST 402", "HIST 403", "HIST 404", "HIST 405", "HIST 406", "HIST 407", "HIST 408", "HIST 409", "HIST 410", "HIST 420"]},
                {"type": "any_of", "courses": ["HIST 191", "HIST 192", "HIST 223", "HIST 240", "HIST 315", "HIST 316", "HIST 319", "HIST 320", "HIST 322", "HIST 323", "HIST 324", "HIST 326", "HIST 327", "HIST 330", "HIST 344", "HIST 352", "HIST 353", "HIST 362", "HIST 368", 
                                                "HIST 420"]}
            ]},
            {"type": "choose_n", "n": 4 , "groups": [
                    {"type": "any_of", "courses": ["HIST 201", "HIST 211", "HIST 212", "HIST 213", "HIST 214", "HIST 215", "HIST 216", "HIST 217", "HIST 218", "HIST 219", "HIST 220", "HIST 221", "HIST 222", "HIST 223", "HIST 224", "HIST 225", "HIST 226", "HIST 228", "HIST 230",
                                                    "HIST 235", "HIST 236", "HIST 237", "HIST 238", "HIST 240", "HIST 241", "HIST 242", "HIST 243", "HIST 255", "HIST 256", "HIST 260", "HIST 261", "HIST 265", "HIST 278", "HIST 279", "HIST 280", "HIST 281", "HIST 282", "HIST 283", 
                                                    "HIST 284", "HIST 299", "HIST 301", "HIST 304", "HIST 306", "HIST 309", "HIST 311", "HIST 312", "HIST 313", "HIST 315", "HIST 316", "HIST 317", "HIST 318", "HIST 319", "HIST 320", "HIST 321", "HIST 322", "HIST 323", "HIST 324", 
                                                    "HIST 325", "HIST 326", "HIST 327", "HIST 330","HIST 331", "HIST 332", "HIST 333", "HIST 334", "HIST 336", "HIST 337", "HIST 341", "HIST 342", "HIST 344", "HIST 345", "HIST 346", "HIST 347", "HIST 348", "HIST 349", "HIST 350", 
                                                    "HIST 351", "HIST 352", "HIST 353", "HIST 355", "HIST 357", "HIST 358", "HIST 359", "HIST 360", "HIST 361", "HIST 362", "HIST 363", "HIST 364", "HIST 367", "HIST 368", "HIST 369", "HIST 370", "HIST 373", "HIST 377", "HIST 378", 
                                                    "HIST 379", "HIST 382", "HIST 383", "HIST 384", "HIST 385", "HIST 386", "HIST 387", "HIST 388", "HIST 391", "HIST 392", "HIST 393", "HIST 394", "HIST 400", "HIST 401", "HIST 402", "HIST 403", "HIST 404", "HIST 405", "HIST 406",
                                                    "HIST 407", "HIST 408", "HIST 409", "HIST 410", "HIST 411", "HIST 412", "HIST 413", "HIST 414", "HIST 467", "HIST 468", "HIST 478", "HIST 479", "HIST 490C", "HIST 491C", "HIST 494", "HIST 495", "HIST 496", "HIST 499"]}
            ]} 
        ] 
    },

    "international relations": {
        "requirements": [
            {"type": "all_of", "courses": ["GOVT 204", "ECON 101", "ECON 102", "GOVT 328", "GOVT 329", "HIST 192", "INRL 300", "INRL 300D"]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["ECON 303", "ECON 304"]},
                {"type": "any_of", "courses": ["ECON 475", "ECON 476"]},
                {"type": "any_of", "courses": ["SOCL 205", "SOCL 313", "SOCL 314"]},
                {"type": "any_of", "courses": ["BUAD 231", "GOVT 301", "GOVT 302", "GOVT 307", "ECON 307", "ECON 308", "PSYC 302", "SOCL 352", "SOCL 353"]},
                {"type": "any_of", "courses": ["ANTH 335", "ANTH 338", "GOVT 311", "GOVT 312", "GOVT 334", "GOVT 335", "GOVT 336", "GOVT 337", "GOVT 338", "GOVT 339", "HIST 280", "HIST 309", "HIST 304", "HIST 325", "HIST 330", "HIST 331", "HIST 332", "HIST 333", "HIST 370",
                                                "HIST 373", "HIST 378", "HIST 384", "HIST 386", "SOCL 312", "SOCL 313"]},
                {"type": "any_of", "courses": ["ECON 481", "ECON 485", "GOVT 402", "GOVT 403", "GOVT 404", "HIST 491C", "GOVT 440", "INRL 491", ]}
            ]},
            {"type": "choose_n", "n": 2, "groups": [
                {"type": "any_of", "courses": ["ANTH 350", "ANTH 475", "ANTH 476", "BUAD 417", "ECON 300", "ECON 342", "ECON 382", "ECON 400", "ECON 474", "ECON 483", "GOVT 203", "GOVT 322", "GOVT 324", "GOVT 325", "GOVT 326", "GOVT 327", "GOVT 330", "GOVT 388", "GOVT 391",
                                               "GOVT 433", "GOVT 482", "HIST 131", "HIST 132", "HIST 142", "HIST 161", "HIST 172", "HIST 181", "HIST 211", "HIST 212", "HIST 223", "HIST 241", "HIST 242", "HIST 243", "HIST 265", "HIST 280", "HIST 284", "HIST 311", "HIST 312",
                                               "HIST 317", "HIST 319", "HIST 325", "HIST 327", "HIST 334", "HIST 341", "HIST 352", "HIST 353", "HIST 413", "HIST 414", "HIST 490C", "HIST 491C", "INRL 100", "INRL 150", "INRL 390", "INRL 480", "PSYC 470", "SOCL 205", "SOCL 318",
                                               "SOCL 340", "SOCL 408", "SOCL 427"]}
                                               
            ]}
        ]
    },

     "kinesiology": {
        "requirements": [
            {"type": "all_of", "courses": ["BIOL 203", "BIOL 203L", "KINE 303", "KINE 304"]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["KINE 308", "KINE 394"]},
                {"type": "any_of", "courses": ["KINE 393", "KINE 401", "KINE 405", "KINE 406", "KINE 455","KINE 493"]}
            ]},
            {"type": "choose_n", "n": 8, "groups": [
                {"type": "any_of", "courses": ["KINE 200", "KINE 270", "KINE 280", "KINE 290", "KINE 295", "KINE 300", "KINE 301", "KINE 303", "KINE 304", "KINE 305", "KINE 308", "KINE 314", "KINE 315", "KINE 320", "KINE 321", "KINE 322", "KINE 340", "KINE 350", "KINE 360",
                                                "KINE 380", "KINE 393", "KINE 404", "KINE 405", "KINE 422", "KINE 442", "KINE 450", "KINE 455", "KINE 493", "KINE 494"]}
                                               
            ]}
        ]
    },
    
    "data science": {
        "requirements": [
            {"type": "all_of", "courses": ["DATA 101", "DATA 201", "DATA 301", "DATA 302", "DATA 303", "MATH 111", "MATH 112", "MATH 211", "MATH 351", "MATH 352"]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["DATA 202", "PHIL 215", "PHIL 303", "PHIL 330"]},
                {"type": "any_of", "courses": ["DATA 420", "DATA 430", "DATA 431", "DATA 440", "DATA 441", "DATA 442", "DATA 444", "DATA 445", "DATA 449"]}
            ]},
            {"type": "choose_n", "n": 3, "groups": [
                {"type": "any_of", "courses": ["DATA 341", "DATA 340", "DATA 441", "DATA 431", "DATA 440", "DATA 442", "DATA 444"]}
                                               
            ]}
        ]
    } 
}

minors_dict = {
    "data science": {
        "requirements": [
            {"type": "all_of", "courses": ["DATA 101", "DATA 201", "DATA 301"]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["DATA 202", "PHIL 215", "PHIL 303", "PHIL 330"]}
            ]},
            {"type": "choose_n", "n": 2, "groups": [
                {"type": "any_of", "courses": [ "BIOL 325", "BIOL 327", "BIOL 445", "BUAD 350", "BUAD 351", "BUAD 352", "BUAD 460", "BUAD 463", "BUAD 466", "BUAD 467", "BUAD 468", "BUAD 469", "CONS 420", "CSCI 215", "DATA 302", "DATA 303", "DATA 320", "DATA 330", "DATA 340",
                                                "DATA 341", "DATA 380", "DATA 390", "DATA 420", "DATA 430", "DATA 431", "DATA 440", "DATA 441", "DATA 442", "DATA 443", "DATA 444", "DATA 445", "DATA 446", "DATA 447", "DATA 448", "DATA 449", "DATA 480", "ECON 308", "ECON 331", 
                                                "ECON 407", "ECON 408", "ECON 413", "ECON 412", "GIS 201", "GIS 405", "GIS 410", "GIS 420", "GOVT 301", "GOVT 302", "GOVT 307", "MATH 309", "MATH 323", "MATH 332", "MATH 351", "MATH 352", "MATH 353", "MATH 408", "MATH 417", 
                                                "MATH 424", "MATH 451", "MATH 452", "MATH 455", "MATH 465", "PSYC 302" ]}
            ]}
        ]
    }, 

     "psychology": {
        "requirements": [
            {"type": "all_of", "courses": ["PSYC 201", "PSYC 202"]},
            {"type": "choose_n", "n": 2, "groups": [
                {"type": "any_of", "courses": ["PSYC 310", "PSYC 312", "PSYC 314", "PSYC 318"]},
                {"type": "any_of", "courses": ["PSYC 311", "PSYC 313", "PSYC 315", "PSYC 317"]}
            ]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["PSYC 350", "PSYC 351", "PSYC 352", "PSYC 353", "PSYC 354", "PSYC 355", "PSYC 356", "PSYC 358", "PSYC 360", "PSYC 362", "PSYC 370", "PSYC 402", "PSYC 404", "PSYC 406", "PSYC 442", "PSYC 445", "PSYC 447", "PSYC 448", "PSYC 448", 
                                               "PSYC 449", "PSYC 450", "PSYC 452", "PSYC 453", "PSYC 454", "PSYC 455", "PSYC 456", "PSYC 457", "PSYC 470", "PSYC 480", "BUAD 442"]}
            ]}
        ]
    }, 

    "mathematics": {
        "requirements": [
            {"type": "choose_n", "n": 4, "groups": [
                {"type": "any_of", "courses": ["MATH 111", "MATH 112", "MATH 131", "MATH 132", "MATH 211", "MATH 212", "MATH 213", "MATH 214", "MATH 265", "MATH 300", "MATH 302", "MATH 307", "MATH 309", "MATH 311", "MATH 323", "MATH 345", "MATH 351", "MATH 352", "MATH 380", 
                                               "MATH 401", "MATH 402", "MATH 405", "MATH 410", "MATH 412", "MATH 413", "MATH 414", "MATH 416", "MATH 417", "MATH 424", "MATH 426", "MATH 428", "MATH 430", "MATH 432", "MATH 441", "MATH 442", "MATH 451", "MATH 452", "MATH 459", 
                                               "MATH 490"]}
            ]},
            {"type": "choose_n", "n": 2, "groups": [
                {"type": "any_of", "courses": ["MATH 302", "MATH 307", "MATH 309", "MATH 311", "MATH 323", "MATH 345", "MATH 351", "MATH 352", "MATH 380", 
                                               "MATH 401", "MATH 402", "MATH 405", "MATH 410", "MATH 412", "MATH 413", "MATH 414", "MATH 416", "MATH 417", "MATH 424", "MATH 426", "MATH 428", "MATH 430", "MATH 432", "MATH 441", "MATH 442", "MATH 451", "MATH 452", "MATH 459", 
                                               "MATH 490"]}
            ]}
        ]
    },

     "history": {
        "requirements": [
            {"type": "choose_n", "n": 4, "groups": [
                {"type": "any_of", "courses": ["HIST 201", "HIST 211", "HIST 212", "HIST 213", "HIST 214", "HIST 215", "HIST 216", "HIST 217", "HIST 218", "HIST 219", "HIST 220", "HIST 221", "HIST 222", "HIST 223", "HIST 224", "HIST 225", "HIST 226", "HIST 228", "HIST 230",
                                                "HIST 235", "HIST 236", "HIST 237", "HIST 238", "HIST 240", "HIST 241", "HIST 242", "HIST 243", "HIST 255", "HIST 256", "HIST 260", "HIST 261", "HIST 265", "HIST 278", "HIST 279", "HIST 280", "HIST 281", "HIST 282", "HIST 283", 
                                                "HIST 284", "HIST 299", "HIST 301", "HIST 304", "HIST 306", "HIST 309", "HIST 311", "HIST 312", "HIST 313", "HIST 315", "HIST 316", "HIST 317", "HIST 318", "HIST 319", "HIST 320", "HIST 321", "HIST 322", "HIST 323", "HIST 324", 
                                                "HIST 325", "HIST 326", "HIST 327", "HIST 330","HIST 331", "HIST 332", "HIST 333", "HIST 334", "HIST 336", "HIST 337", "HIST 341", "HIST 342", "HIST 344", "HIST 345", "HIST 346", "HIST 347", "HIST 348", "HIST 349", "HIST 350", 
                                                "HIST 351", "HIST 352", "HIST 353", "HIST 355", "HIST 357", "HIST 358", "HIST 359", "HIST 360", "HIST 361", "HIST 362", "HIST 363", "HIST 364", "HIST 367", "HIST 368", "HIST 369", "HIST 370", "HIST 373", "HIST 377", "HIST 378", 
                                                "HIST 379", "HIST 382", "HIST 383", "HIST 384", "HIST 385", "HIST 386", "HIST 387", "HIST 388", "HIST 391", "HIST 392", "HIST 393", "HIST 394", "HIST 400", "HIST 401", "HIST 402", "HIST 403", "HIST 404", "HIST 405", "HIST 406",
                                                "HIST 407", "HIST 408", "HIST 409", "HIST 410", "HIST 411", "HIST 412", "HIST 413", "HIST 414", "HIST 467", "HIST 468", "HIST 478", "HIST 479", "HIST 490C", "HIST 491C"]}
            ]},
            {"type": "choose_n", "n": 2, "groups": [
                {"type": "any_of", "courses": ["HIST 100", "HIST 111", "HIST 112", "HIST 121", "HIST 122", "HIST 131", "HIST 132", "HIST 141", "HIST 142", "HIST 150", "HIST 161", "HIST 171", "HIST 172", "HIST 181", "HIST 191", "HIST 192", "HIST 201", "HIST 211", "HIST 212", 
                                               "HIST 213", "HIST 214", "HIST 215", "HIST 216", "HIST 217", "HIST 218", "HIST 219", "HIST 220", "HIST 221", "HIST 222", "HIST 223", "HIST 224", "HIST 225", "HIST 226", "HIST 228", "HIST 230", "HIST 235", "HIST 236", "HIST 237", 
                                               "HIST 238", "HIST 240", "HIST 241", "HIST 242", "HIST 243", "HIST 255", "HIST 256", "HIST 260", "HIST 261", "HIST 265", "HIST 278", "HIST 279", "HIST 280", "HIST 281", "HIST 282", "HIST 283", "HIST 284", "HIST 299", "HIST 301", 
                                               "HIST 304", "HIST 306", "HIST 309", "HIST 311", "HIST 312", "HIST 313", "HIST 315", "HIST 316", "HIST 317", "HIST 318", "HIST 319", "HIST 320", "HIST 321", "HIST 322", "HIST 323", "HIST 324", "HIST 325", "HIST 326", "HIST 327", 
                                               "HIST 330","HIST 331", "HIST 332", "HIST 333", "HIST 334", "HIST 336", "HIST 337", "HIST 341", "HIST 342", "HIST 344", "HIST 345", "HIST 346", "HIST 347", "HIST 348", "HIST 349", "HIST 350", "HIST 351", "HIST 352", "HIST 353", 
                                               "HIST 355", "HIST 357", "HIST 358", "HIST 359", "HIST 360", "HIST 361", "HIST 362", "HIST 363", "HIST 364", "HIST 367", "HIST 368", "HIST 369", "HIST 370", "HIST 373", "HIST 377", "HIST 378", "HIST 379", "HIST 382", "HIST 383", 
                                               "HIST 384", "HIST 385", "HIST 386", "HIST 387", "HIST 388", "HIST 391", "HIST 392", "HIST 393", "HIST 394", "HIST 400", "HIST 401", "HIST 402", "HIST 403", "HIST 404", "HIST 405", "HIST 406", "HIST 407", "HIST 408", "HIST 409", 
                                               "HIST 410", "HIST 411", "HIST 412", "HIST 413", "HIST 414", "HIST 467", "HIST 468", "HIST 478", "HIST 479", "HIST 490C", "HIST 491C"]}
            ]}
        ]
    }, 

     "biochemistry": {
        "requirements": [
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ['CHEM 103','CHEM 206', "CHEM 207", "CHEM 209", "CHEM 307"]},
                {"type": "any_of", "courses": ["BIOL 225", "BIOL 203"]},
                {"type": "any_of", "courses": ["BIOL 220", "BIOL 204", "CHEM 208", "CHEM 305", "CHEM 308", "CHEM 335"]},
                {"type": "any_of", "courses": ["CHEM 314", "CHEM 414", "BIOL 314", "BIOL 414"]},
                {"type": "any_of", "courses": ["BIOL 306", "BIOL 310", "BIOL 345", "BIOL 415", "BIOL 420", "BIOL 433", "BIOL 437", "BIOL 442", "BIOL 453"]},
                {"type": "any_of", "courses": ["CHEM 309", "CHEM 341", "CHEM 415", "CHEM 417", "CHEM 419", "CHEM 453"]}
            ]}
        ]
    },
    "management and organizational leadership": {
        "requirements": [
            {"type": "all_of", "courses": ["BUAD 317"]},
            {"type": "choose_n", "n": 3, "groups": [
                {"type": "any_of", "courses": ["BUAD 430", "BAUD 431", "BAUD 435", "BUAD 436", "BAUD 437", "BUAD 438", "BUAD 442"]}
            ]},
            {"type": "choose_n", "n": 2, "groups": [
                {"type": "any_of", "courses": ["BUAD 203", "BUAD 300", "BUAD 301", "BUAD 302", "BUAD 303", "BUAD 311", "BUAD 317", "BUAD 323", "BUAD 324", "BUAD 325", "BUAD 328", "BUAD 330", "BUAD 342", "BUAD 343", "BUAD 350", "BUAD 351", "BUAD 352", "BUAD 401", "BUAD 404", 
                                               "BUAD 405", "BUAD 406", "BUAD 408", "BUAD 410", "BUAD 412", "BUAD 413", "BUAD 417", "BUAD 419", "BUAD 421", "BUAD 423", "BUAD 430", "BUAD 431", "BUAD 432", "BUAD 434", "BUAD 435", "BUAD 436", "BUAD 437", "BUAD 438", "BUAD 442", 
                                               "BUAD 443", "BUAD 446", "BUAD 447", "BUAD 448", "BUAD 450", "BUAD 452", "BUAD 454", "BUAD 456", "BUAD 549", "BUAD 461", "BUAD 462", "BUAD 465", "BUAD 466", "BUAD 467", "BUAD 468", "BUAD 469", "BUAD 474", "BUAD 476", "BUAD 480", 
                                               "BUAD 481", "BUAD 482", "BUAD 490", "BUAD 492"]}
            ]}
        ]
    }, 
    "chemistry": {
        "requirements": [
            {"type": "all_of", "courses": ["CHEM 103", "CHEM 208", "CHEM 103L", "CHEM 206", "CHEM 206L", "CHEM 207", "CHEM 209", "CHEM 253"]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["CHEM 254", "CHEM 256"]},
                {"type": "any_of", "courses": ["CHEM 301", "CHEM 309", "CHEM 312", "CHEM 341", "CHEM 361"]},
                {"type": "any_of", "courses": ["CHEM 314", "CHEM 403", "CHEM 411", "CHEM 457"]}

            ]}
        ]
    }, 
    "kinesiology": {
        "requirements": [
            {"type": "all_of", "courses": ["BIOL 203", "BIOL 203L", "KINE 303", "KINE 304"]},
            {"type": "choose_n", "n": 5, "groups": [
                {"type": "any_of", "courses": ["KINE 200", "KINE 204", "KINE 240", "KINE 270", "KINE 280", "KINE 290", "KINE 295", "KINE 300", "KINE 301", "KINE 303", "KINE 304", "KINE 305", "KINE 308", "KINE 314", "KINE 315", "KINE 320", "KINE 321", "KINE 322", "KINE 335", 
                                               "KINE 340", "KINE 350", "KINE 352", "KINE 360", "KINE 365", "KINE 380", "KINE 393", "KINE 394", "KINE 405", "KINE 422", "KINE 442", "KINE 450", "KINE 455", "KINE 485", "KINE 493", "KINE 494"]}

            ]}
        ]
    }, 
    "business analytics": {
        "requirements": [
            {"type": "all_of", "courses": ["BUAD 231", "BUAD 330", "BUAD 350", "BUAD 351", "BUAD 352", "BUAD 466", "BUAD 467", "BUAD 468"]},
            {"type": "choose_n", "n": 1, "groups": [
                {"type": "any_of", "courses": ["BUAD 460", "BUAD 461", "BUAD 462", "BUAD 463", "BUAD 465", "BUAD 467", "BUAD 469", "BUAD 482"]}

            ]}
        ]
    }, 
     "biology": {
        "requirements": [
            {"type": "all_of", "courses": ["BIOL 203", "BIOL 203L", "BIOL 204", "BIOL 204L"]},
            {"type": "choose_n", "n": 5, "groups": [
                {"type": "any_of", "courses": ["BIOL 301", "BIOL 302", "BIOL 304", "BIOL 305", "BIOL 306", "BIOL 310", "BIOL 311", "BIOL 312", "BIOL 312F", "BIOL 314", "BIOL 317", "BIOL 318", "BIOL 325", "BIOL 327", "BIOL 330", "BIOL 340", "BIOL 345", "BIOL 351", "BIOL 356", 
                                               "BIOL 377", "BIOL 401", "BIOL 404", "BIOL 405", "BIOL 406", "BIOL 407", "BIOL 408", "BIOL 409", "BIOL 410", "BIOL 411", "BIOL 412", "BIOL 413", "BIOL 413L", "BIOL 415", "BIOL 416", "BIOL 417", "BIOL 418", "BIOL 419", "BIOL 420", 
                                               "BIOL 426", "BIOL 427", "BIOL 428", "BIOL 430", "BIOL 432", "BIOL 432L", "BIOL 433", "BIOL 437", "BIOL 438", "BIOL 442", "BIOL 443", "BIOL 444", "BIOL 445", "BIOL 451", "BIOL 453", "BIOL 453L", "BIOL 454", "BIOL 455", "BIOL 456", 
                                               "BIOL 456L", "BIOL 457", "BIOL 458", "BIOL 459", "BIOL 460", "BIOL 461"]}

            ]}
        ]
    }, 
    

}


minors_list = list(minors_dict.keys())
majors_list =  list(majors_dict.keys())
os.makedirs("data", exist_ok=True)
np.save(os.path.join("data", 'majors.npy'), majors_dict)
np.save(os.path.join("data", 'majors_list.npy'), majors_list)
np.save(os.path.join("data", 'minors.npy'), minors_dict)
np.save(os.path.join("data", 'minors_list.npy'), minors_list)
