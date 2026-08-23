document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       ELEMENTS
    ===================================================== */

    const windows =
        document.querySelectorAll(
            ".portfolio-window, .resume-dialog"
        );


    const desktopIcons =
        document.querySelectorAll(
            ".desktop-icon"
        );


    const dockItems =
        document.querySelectorAll(
            ".dock-item"
        );


    const clock =
        document.getElementById("clock");


    /* =====================================================
       CLOSE ALL WINDOWS
    ===================================================== */

    function closeAllWindows() {

        windows.forEach((windowElement) => {

            windowElement.classList.remove(
                "open"
            );

        });

    }


    /* =====================================================
       OPEN WINDOW
    ===================================================== */

    function openWindow(windowName) {

        closeAllWindows();


        const target =
            document.getElementById(
                `${windowName}-window`
            );


        if (!target) {
            return;
        }


        target.classList.add("open");

    }


    /* =====================================================
       DESKTOP ICONS
    ===================================================== */

    desktopIcons.forEach((icon) => {

        icon.addEventListener(
            "click",
            () => {

                const windowName =
                    icon.dataset.window;


                if (!windowName) {
                    return;
                }


                openWindow(windowName);

            }
        );

    });


    /* =====================================================
       DOCK
    ===================================================== */

    dockItems.forEach((item) => {

        item.addEventListener(
            "click",
            () => {

                const windowName =
                    item.dataset.window;


                if (!windowName) {
                    return;
                }


                openWindow(windowName);

            }
        );

    });


    /* =====================================================
       CLOSE BUTTONS
    ===================================================== */

    document
        .querySelectorAll(
            ".window-close, .resume-dialog-close"
        )
        .forEach((button) => {

            button.addEventListener(
                "click",
                () => {

                    const windowElement =
                        button.closest(
                            ".portfolio-window, .resume-dialog"
                        );


                    if (windowElement) {

                        windowElement.classList.remove(
                            "open"
                        );

                    }

                }
            );

        });


    /* =====================================================
       ASK ME
    ===================================================== */

    const askInput =
        document.getElementById(
            "ask-input"
        );


    const askSend =
        document.getElementById(
            "ask-send"
        );


    const askForm =
        document.getElementById(
            "ask-form"
        );


    const chatMessages =
        document.getElementById(
            "chat-messages"
        );


    /* =====================================================
       ADD MESSAGE
    ===================================================== */

    function addMessage(
        text,
        type
    ) {

        const message =
            document.createElement(
                "div"
            );


        message.className =
            type === "user"
                ? "user-message"
                : "bot-message";


        message.textContent =
            text;


        chatMessages.appendChild(
            message
        );


        chatMessages.scrollTop =
            chatMessages.scrollHeight;


        return message;

    }


    /* =====================================================
       SEND QUESTION
    ===================================================== */

    async function sendQuestion(
        suppliedQuestion = null
    ) {

        const question =
            suppliedQuestion ||
            askInput.value.trim();


        if (!question) {
            return;
        }


        /* User message */

        addMessage(
            question,
            "user"
        );


        /* Clear input */

        askInput.value = "";


        /* Disable send */

        askSend.disabled = true;


        /* Thinking */

        const thinking =
            addMessage(
                "Thinking... 🤔",
                "bot"
            );


        try {

            const response =
                await fetch(
                    "http://127.0.0.1:5000/ask",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                question:
                                    question
                            })
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `Server returned ${response.status}`
                );

            }


            const data =
                await response.json();


            thinking.remove();


            addMessage(
                data.answer ||
                "I couldn't generate an answer.",
                "bot"
            );

        }


        catch (error) {

            console.error(
                "Ask Me error:",
                error
            );


            thinking.remove();


            addMessage(
                "I couldn't connect to my AI brain. Please make sure the Python server is running on port 5000.",
                "bot"
            );

        }


        finally {

            askSend.disabled =
                false;


            askInput.focus();

        }

    }


    /* =====================================================
       ASK FORM
    ===================================================== */

    if (askForm) {

        askForm.addEventListener(
            "submit",
            (event) => {

                event.preventDefault();

                sendQuestion();

            }
        );

    }


    /* =====================================================
       QUICK QUESTIONS
    ===================================================== */

    document
        .querySelectorAll(
            ".quick-questions button"
        )
        .forEach((button) => {

            button.addEventListener(
                "click",
                () => {

                    const question =
                        button.dataset.question;


                    sendQuestion(
                        question
                    );

                }
            );

        });


    /* =====================================================
       ESCAPE KEY
    ===================================================== */

    document.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Escape"
            ) {

                closeAllWindows();

            }

        }
    );


    /* =====================================================
       CLOCK
    ===================================================== */

    function updateClock() {

        if (!clock) {
            return;
        }


        const now =
            new Date();


        clock.textContent =
            now.toLocaleTimeString(
                [],
                {
                    hour: "numeric",
                    minute: "2-digit"
                }
            );

    }


    updateClock();


    setInterval(
        updateClock,
        30000
    );

});

