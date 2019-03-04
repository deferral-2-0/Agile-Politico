const partiescontainer = document.getElementById("render-parties");

partiescontainer.appendChild(createElement(loadingindicator));

fetch("https://tevpolitico.herokuapp.com/api/v2/parties")
  .then(data => data.json())
  .then(({ status, data }) => {
    destroyNodeChildren("render-parties");
    if (status === 200) {
      const partiestoBeRendered = {
        type: "ol",
        props: { id: "orderedlistofparties" },
        children: data.map((party, idx) => ({
          type: "li",
          props: { class: "partiesindb" },
          children: [
            {
              type: "span",
              props: {},
              children: [`${idx + 1}.`]
            },
            {
              type: "p",
              props: {},
              children: [`Party Name:  ${party.name}`]
            },
            {
              type: "p",
              props: {},
              children: [`Party Head Quaters:  ${party.hqAddress}`]
            }
          ]
        }))
      };
      partiescontainer.appendChild(createElement(partiestoBeRendered));
    }
  });
