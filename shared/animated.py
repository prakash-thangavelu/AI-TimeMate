import streamlit as st
import json
import time

def success_screen(message="Success!", sub_message="Your action was completed."):
    # Confetti
    st.balloons()

    # Lottie animation
    lottie_json = {
        "v": "5.5.7",
        "fr": 30,
        "ip": 0,
        "op": 60,
        "w": 500,
        "h": 500,
        "nm": "success",
        "ddd": 0,
        "assets": [],
        "layers": [
            {
                "ddd": 0,
                "ind": 1,
                "ty": 4,
                "nm": "Checkmark",
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100},
                    "r": {"a": 0, "k": 0},
                    "p": {"a": 0, "k": [250, 250, 0]},
                    "a": {"a": 0, "k": [0, 0, 0]},
                    "s": {"a": 0, "k": [100, 100, 100]}
                },
                "shapes": [
                    {
                        "ty": "sh",
                        "ks": {
                            "a": 0,
                            "k": {
                                "i": [],
                                "o": [],
                                "v": [
                                    [0, 0],
                                    [50, 50],
                                    [150, -50]
                                ],
                                "c": False
                            }
                        },
                        "nm": "Check Path"
                    }
                ]
            }
        ]
    }

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:20px;
            background:white;
            border-radius:15px;
            box-shadow:0 4px 12px rgba(0,0,0,0.1);
            margin-top:20px;">
            <h2 style="color:#4F46E5;">{message}</h2>
            <p style="color:#374151; font-size:18px;">{sub_message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st_lottie = st.components.v1.html(
        f"""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.7.4/lottie.min.js"></script>
        <div id="lottie" style="width:300px; height:300px; margin:auto;"></div>
        <script>
            var animationData = {json.dumps(lottie_json)};
            var params = {{
                container: document.getElementById('lottie'),
                renderer: 'svg',
                loop: false,
                autoplay: true,
                animationData: animationData
            }};
            var anim = lottie.loadAnimation(params);
        </script>
        """,
        height=350
    )

    time.sleep(1)
