const RPC = require("discord-rpc");
const rpc = new RPC.Client({
    transport: "ipc"
});

rpc.on("ready", () => {
    rpc.setActivity({
        details: "Vibing",
        state: "Meow",
        largeImageKey: "me",
        largeImageText: "Hello World",
        smallImageKey: "me",
        smallImageText: "test"
    });

    console.log("Rich presence active");

});

rpc.login({
    clientId: "752205939628703744"
});
