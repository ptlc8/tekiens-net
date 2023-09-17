sendRequest("GET", "assos.json")
.then(res => {
	var assos = JSON.parse(res);
	var assosDiv = document.getElementById("associations");
	for (let asso of assos) {
		if (asso.end) continue;
		assosDiv.appendChild(createElement("div", {className: "card asso"}, [
			createElement("h3", {}, asso.emoji + " " + asso.name[asso.name.length - 1] + " - " + asso.theme),
			createElement("ul", {}, Object.entries(asso.socials).map(social =>
				createElement("li", {}, [createElement("a", {href: social[1], target: "_blank"}, social[0])])
			)),
			createElement("span", {}, asso.local ? ("Local : " + asso.local + " - " + asso.campus) : asso.campus)
		]));
	}
});
