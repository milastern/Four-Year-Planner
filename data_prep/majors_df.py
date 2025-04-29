import numpy as np
import os


majors = {
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
                    {"type": "any_of", "courses": ["HIST 201", "HIST 211", "HIST 212", "HIST 213", "HIST 214", "HIST 215", "HIST 216", "HIST 217", ]}
                ]} 
        ] 
    }
}


os.makedirs("data", exist_ok=True)
np.save(os.path.join("data", 'majors.npy'), majors)