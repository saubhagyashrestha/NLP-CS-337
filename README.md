# NLP-CS-337
Northwestern University
![Alt text](https://img.shields.io/badge/Hello-World-green)

Should work: <img src = "https://img.shields.io/badge/Good-Morning-green" />

Should not work: <img src = "https://lol" />

Should work with no alt: <img src='https://img.shields.io/badge/Good-Night-green' oneerror = "this.oneerror=null;this.alt = 'Image not found';"/>

Should work with alt: <img src = 'https://img.shields.io/badge/Good-Evening-green' alt = 'Good evening' />

Should not work and then should redirect: <img src = "https://lol" onerror="this.onerror=null;this.src='https://img.shields.io/badge/Good-Night-green';" />

Should not work and then have alt message 'nope' : <img src = "https://lol" alt = 'yes' onerror="this.onerror=null;this.alt ='nope';" />

Should not work and then should redirect with alt: <img src="https://lol" onerror="this.onerror=null;this.alt = 'Image not found';this.src='https://img.shields.io/badge/Good-Night-green';" />
