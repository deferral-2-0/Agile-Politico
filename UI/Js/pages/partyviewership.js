const partiescontainer = document.getElementById("render-parties");
const allparties = [
  {
    datecreated: new Date(),
    name: "House Stark",
    representative: "Jon Snow",
    motto: "Winter is Coming"
  },
  {
    datecreated: new Date(),
    name: "House Lannister",
    representative: "Cercei Lannister",
    motto: "Hear my roar"
  },
  {
    datecreated: new Date(),
    name: "House Baratheon",
    representative: "Gendry",
    motto: "Our's is the fury"
  }
];

fetch("https://tevpolitico.herokuapp.com/api/v2/parties")
  .then(data => data.json())
  .then(({ status, data }) => {
    if (status === 200) {
      const partiestoBeRendered = {
        type: "ol",
        props: {},
        children: data.map((party, idx) => ({
          type: "li",
          props: {},
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
