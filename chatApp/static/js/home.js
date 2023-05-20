const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let current_convo = "";

const requestDjango = async (url, method, body) => {
  headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
  };
  if (method == "post") {
    const csrf = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    headers["X-CSRFToken"] = csrf;
  }
  let response = await fetch(url, {
    method: method,
    headers: headers,
    body: body,
  });

  return response.json();
};

const getChatData = async () => {
  let url = "http://127.0.0.1:8000/chats_data/";

  let data = await requestDjango(url, "get");
  console.log(data);
  create_request_list(data.request_list);
  create_friends_list(data.friends_list);
};

const sendRequest = async (event) => {
  let id = event.target.classList[1];
  let url = "http://127.0.0.1:8000/send_request/" + id;

  let data = await requestDjango(url, "get");
  console.log(await data);

  if (data.request_sent) {
    event.target.innerText = "Sent success";
    await sleep(2000);

    const request = document.getElementById(id).remove();
  }
};

const create_request_list = (listArray) => {
  const ulElement = document.getElementById("request_list");
  ulElement.innerText = "";

  listArray.forEach((member) => {
    li = createElementAddClass("li", "request");
    li.id = member.username + "accept";

    infoDiv = createElementAddClass("div", "info");

    nameDiv = createElementAddClass("div", "name");

    strong = document.createElement("strong");
    strong.innerText = member.username;

    nameDiv.appendChild(strong);

    actionDiv = createElementAddClass("div", "action");

    acceptSpan = createElementAddClass("span", "accept");
    acceptSpan.innerText = "accept";

    acceptSpan.addEventListener(
      "click",
      async () => await actionRequest("accept", member.username)
    );

    rejectSpan = createElementAddClass("span", "reject");
    rejectSpan.innerText = "reject";

    rejectSpan.addEventListener(
      "click",
      async () => await actionRequest("reject", member.username)
    );

    actionDiv.appendChild(acceptSpan);
    actionDiv.appendChild(rejectSpan);

    infoDiv.appendChild(nameDiv);
    infoDiv.appendChild(actionDiv);

    profileDiv = createElementAddClass("div", "profile_img");

    imgEle = document.createElement("img");
    imgEle.setAttribute("src", member.picture);
    imgEle.setAttribute("alt", "picture");

    profileDiv.appendChild(imgEle);

    li.appendChild(infoDiv);
    li.appendChild(profileDiv);

    ulElement.appendChild(li);
  });
};

const create_friends_list = (listArray) => {
  const ulElement = document.getElementById("friends_list");

  ulElement.innerText = "";

  listArray.forEach((member) => {
    li = createElementAddClass("li", "friend");

    li.addEventListener("click", () => {
      getConvos(member.username);
      current_convo = member.username;
    });

    infoDiv = createElementAddClass("div", "name_message");

    nameDiv = createElementAddClass("div", "name");
    messageDiv = createElementAddClass("div", "message");

    if (member.last_message) {
      if (member.last_message.seen === true) {
        nameDiv.innerText = member.username;
        messageDiv.innerText =
          member.last_message.message.length > 17
            ? member.last_message.message.slice(0, 17) + "..."
            : member.last_message.message + "...";
      } else if (member.last_message.seen === false) {
        nameStrong = document.createElement("strong");
        nameStrong.innerText = member.username;

        messageStrong = document.createElement("strong");
        messageStrong.innerText =
          member.last_message.message.length > 17
            ? member.last_message.message.slice(0, 17) + "..."
            : member.last_message.message + "...";

        nameDiv.appendChild(nameStrong);
        messageDiv.appendChild(messageStrong);
      } else {
        nameDiv.innerText = member.username;
        messageDiv.innerText =
          member.last_message.message.length > 17
            ? member.last_message.message.slice(0, 17) + "..."
            : member.last_message.message + "...";
      }
    } else {
      nameDiv.innerText = member.username;
      messageDiv.innerHTML = "<br />";
    }

    infoDiv.appendChild(nameDiv);
    infoDiv.appendChild(messageDiv);

    profileDiv = createElementAddClass("div", "profile_img");

    imgEle = document.createElement("img");
    imgEle.setAttribute("src", member.picture);
    imgEle.setAttribute("alt", "picture");

    profileDiv.appendChild(imgEle);

    li.appendChild(infoDiv);
    li.appendChild(profileDiv);

    ulElement.appendChild(li);
  });
};

const getConvos = (username) => {
  url = "http://127.0.0.1:8000/get_convo/" + username + "/";

  fetch(url, {
    method: "get",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/json",
    },
  }).then((response) =>
    response.json().then((data) => createConvos(username, data))
  );
};

const createConvos = (username, data) => {
  const sectionElement = document.getElementById("chat_section");
  const messageForm = document.querySelector(".message_form");
  messageForm.style.display = "block";

  sectionElement.innerText = "";

  nameDiv = createElementAddClass("div", "friend_name");
  nameDiv.id = "chatter";
  strong = document.createElement("strong");
  strong.innerText = username;

  nameDiv.appendChild(strong);
  sectionElement.appendChild(nameDiv);

  if (!data) {
    startDiv = createElementAddClass("div", "start_chat");
    startDiv.innerHTML =
      "No messages here :( <br> Send a message to start a conversation";

    sectionElement.appendChild(startDiv);
    return;
  }
  console.log(data);

  bodyDiv = createElementAddClass("div", "chat_body");

  data.forEach((chat) => {
    if (chat.is_user) chatDiv = createElementAddClass("div", "right_send");
    else chatDiv = createElementAddClass("div", "left_recieve");

    chatDiv.innerHTML = chat.message;
    bodyDiv.appendChild(chatDiv);
  });

  sectionElement.appendChild(bodyDiv);
};

const createElementAddClass = (element, className) => {
  tempEle = document.createElement(element);
  tempEle.classList.add(className);
  return tempEle;
};

const actionRequest = async (action, id) => {
  let url = "http://127.0.0.1:8000/request_action/" + action + "_" + id;
  console.log(url);
  await fetch(url, {
    method: "get",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/json",
    },
  }).then((response) =>
    response.json().then((responseJson) => {
      if (responseJson.accepted) {
        let liEle = document.getElementById(id + "accept");
        liEle.innerText = "Request Accepted";

        sleep(2000);
        liEle.remove();
      }
    })
  );
};

const sendMessage = () => {
  const textareaElement = document.getElementById("message");
  const sent_to = document.getElementById("chatter").innerText;
  const csrf_token = document.querySelector(
    '[name="csrfmiddlewaretoken"]'
  ).value;
  if (message) {
    let url = "http://127.0.0.1:8000/send_message/";
    body = {
      sent_to: sent_to,
      message: textareaElement.value,
    };
    fetch(url, {
      method: "post",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
      },
      body: JSON.stringify(body),
    }).then((response) => response.json().then((data) => console.log(data)));

    textareaElement.value = "";
    textareaElement.focus();
  }
};

const runMain = () => {
  getChatData();
  if (current_convo) {
    getConvos(current_convo);
  }
};

setInterval(runMain, 3000);
// getChatData();
