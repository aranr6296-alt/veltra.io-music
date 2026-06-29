import { useState, useRef, useEffect } from "react";

const DISCORD_COLORS = {
  bg: "#313338",
  sidebar: "#2B2D31",
  serverBar: "#1E1F22",
  channelBg: "#313338",
  messageBg: "#313338",
  inputBg: "#383A40",
  header: "#2B2D31",
  text: "#DBDEE1",
  muted: "#80848E",
  accent: "#5865F2",
  accentHover: "#4752C4",
  mention: "#F0B232",
  online: "#23A55A",
  idle: "#F0B232",
  dnd: "#F23F43",
  offline: "#80848E",
  luna: "#7C6FF7",
  lunaGlow: "#9B8EFF",
  success: "#23A55A",
  danger: "#DA373C",
  gold: "#FFD700",
  cardBg: "#2B2D31",
  divider: "#3F4147",
};

const LUNA_COMMANDS = [
  { name: "!help", desc: "Shows all available commands", category: "General" },
  { name: "!play <song>", desc: "Play music in your voice channel", category: "Music" },
  { name: "!skip", desc: "Skip the current song", category: "Music" },
  { name: "!queue", desc: "Show the music queue", category: "Music" },
  { name: "!volume <1-100>", desc: "Set the volume", category: "Music" },
  { name: "!ban <user>", desc: "Ban a user from the server", category: "Moderation" },
  { name: "!kick <user>", desc: "Kick a user from the server", category: "Moderation" },
  { name: "!mute <user>", desc: "Mute a user", category: "Moderation" },
  { name: "!warn <user>", desc: "Warn a user", category: "Moderation" },
  { name: "!clear <amount>", desc: "Clear messages in a channel", category: "Moderation" },
  { name: "!rank", desc: "Show your server rank & XP", category: "Leveling" },
  { name: "!leaderboard", desc: "Show the top 10 members", category: "Leveling" },
  { name: "!daily", desc: "Claim your daily coins", category: "Economy" },
  { name: "!balance", desc: "Check your coin balance", category: "Economy" },
  { name: "!give <user> <amount>", desc: "Give coins to a user", category: "Economy" },
  { name: "!poll <question>", desc: "Create a poll", category: "Utility" },
  { name: "!remind <time> <msg>", desc: "Set a reminder", category: "Utility" },
  { name: "!weather <city>", desc: "Get weather info", category: "Utility" },
  { name: "!avatar <user>", desc: "Get a user's avatar", category: "Fun" },
  { name: "!8ball <question>", desc: "Ask the magic 8ball", category: "Fun" },
  { name: "!coinflip", desc: "Flip a coin", category: "Fun" },
  { name: "!joke", desc: "Get a random joke", category: "Fun" },
];

const SERVERS = [
  { id: 1, name: "Luna Support", icon: "🌙", notifications: 3 },
  { id: 2, name: "Gaming Hub", icon: "🎮", notifications: 0 },
  { id: 3, name: "Music Lounge", icon: "🎵", notifications: 12 },
  { id: 4, name: "Dev Corner", icon: "💻", notifications: 0 },
];

const CHANNELS = [
  { id: 1, name: "general", type: "text", category: "TEXT CHANNELS" },
  { id: 2, name: "announcements", type: "text", category: "TEXT CHANNELS" },
  { id: 3, name: "luna-commands", type: "text", category: "TEXT CHANNELS" },
  { id: 4, name: "music-requests", type: "text", category: "MUSIC" },
  { id: 5, name: "🔊 General Voice", type: "voice", category: "VOICE CHANNELS" },
  { id: 6, name: "🔊 Music Room", type: "voice", category: "VOICE CHANNELS" },
];

const MEMBERS = [
  { id: 1, name: "Luna Bot", tag: "0001", status: "online", role: "Bot", color: DISCORD_COLORS.lunaGlow, isBot: true },
  { id: 2, name: "ServerOwner", tag: "1337", status: "online", role: "Admin", color: "#F23F43" },
  { id: 3, name: "xX_Gamer_Xx", tag: "4269", status: "idle", role: "Member", color: DISCORD_COLORS.text },
  { id: 4, name: "MusicLover", tag: "7823", status: "dnd", role: "DJ", color: "#F0B232" },
  { id: 5, name: "CodeWizard", tag: "0042", status: "offline", role: "Member", color: DISCORD_COLORS.text },
];

const JOKES = [
  "Why don't scientists trust atoms? Because they make up everything!",
  "I told my wife she was drawing her eyebrows too high. She looked surprised.",
  "Why don't eggs tell jokes? They'd crack each other up.",
  "I'm reading a book about anti-gravity. It's impossible to put down!",
];

const EIGHTBALL = [
  "It is certain.", "Without a doubt.", "Yes, definitely!", "Signs point to yes.",
  "Reply hazy, try again.", "Cannot predict now.", "Concentrate and ask again.",
  "Don't count on it.", "Very doubtful.", "My sources say no.",
];

function generateLunaResponse(input, messages) {
  const lower = input.toLowerCase().trim();
  const ts = () => new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  if (lower.startsWith("!help")) {
    return {
      id: Date.now(),
      author: "Luna Bot",
      isBot: true,
      avatar: "🌙",
      timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.luna,
        title: "🌙 Luna Bot — Command List",
        description: "Here are all my commands! Prefix: `!`",
        fields: [
          { name: "🎵 Music", value: "`!play` `!skip` `!queue` `!volume`" },
          { name: "🛡️ Moderation", value: "`!ban` `!kick` `!mute` `!warn` `!clear`" },
          { name: "📊 Leveling", value: "`!rank` `!leaderboard`" },
          { name: "💰 Economy", value: "`!daily` `!balance` `!give`" },
          { name: "🔧 Utility", value: "`!poll` `!remind` `!weather`" },
          { name: "🎲 Fun", value: "`!8ball` `!coinflip` `!joke` `!avatar`" },
        ],
        footer: "Luna Bot v2.4.1 • Made with 💜",
      },
    };
  }

  if (lower.startsWith("!play ")) {
    const song = input.slice(6).trim() || "Unknown Song";
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.success,
        title: "🎵 Now Playing",
        description: `**${song}**`,
        fields: [
          { name: "Duration", value: "3:42" },
          { name: "Requested by", value: "You" },
          { name: "Queue Position", value: "#1" },
        ],
        footer: "Use !skip to skip • !queue to view queue",
      },
    };
  }

  if (lower === "!queue") {
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.luna,
        title: "🎵 Music Queue",
        description: "**Now Playing:**\n🎵 Lo-fi Chill Mix — 3:42\n\n**Up Next:**\n1. Midnight Vibes — 4:12\n2. Chill Hop Beats — 5:30\n3. Rainy Day Jazz — 3:58",
        footer: "3 songs in queue",
      },
    };
  }

  if (lower === "!skip") {
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      content: "⏭️ Skipped! Now playing: **Midnight Vibes**",
    };
  }

  if (lower === "!rank") {
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.gold,
        title: "📊 Your Rank",
        fields: [
          { name: "🏆 Rank", value: "#42 on this server" },
          { name: "⭐ Level", value: "Level 17" },
          { name: "✨ XP", value: "8,420 / 10,000 XP" },
          { name: "💬 Messages", value: "1,337 messages" },
        ],
        footer: "Keep chatting to level up!",
      },
    };
  }

  if (lower === "!leaderboard") {
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.gold,
        title: "🏆 Server Leaderboard",
        description:
          "🥇 **ServerOwner** — Level 50 (99,999 XP)\n🥈 **MusicLover** — Level 32 (48,200 XP)\n🥉 **xX_Gamer_Xx** — Level 24 (22,100 XP)\n4. **CodeWizard** — Level 19 (11,500 XP)\n5. **You** — Level 17 (8,420 XP)",
        footer: "Updated every 10 minutes",
      },
    };
  }

  if (lower === "!daily") {
    const coins = Math.floor(Math.random() * 500) + 100;
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.gold,
        title: "💰 Daily Reward!",
        description: `You received **${coins} coins**! Come back tomorrow for more.`,
        fields: [{ name: "New Balance", value: `${10000 + coins} coins` }],
        footer: "Daily reset: 24 hours",
      },
    };
  }

  if (lower === "!balance") {
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.gold,
        title: "💰 Wallet",
        fields: [
          { name: "Coins", value: "10,000 🪙" },
          { name: "Bank", value: "50,000 🏦" },
          { name: "Total", value: "60,000 💎" },
        ],
      },
    };
  }

  if (lower === "!coinflip") {
    const result = Math.random() > 0.5 ? "Heads 🪙" : "Tails 🪙";
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      content: `🪙 The coin landed on **${result}**!`,
    };
  }

  if (lower === "!joke") {
    const joke = JOKES[Math.floor(Math.random() * JOKES.length)];
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.luna,
        title: "😂 Here's a joke!",
        description: joke,
      },
    };
  }

  if (lower.startsWith("!8ball ")) {
    const q = input.slice(7).trim();
    const answer = EIGHTBALL[Math.floor(Math.random() * EIGHTBALL.length)];
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.luna,
        title: "🎱 Magic 8-Ball",
        fields: [
          { name: "Question", value: q || "..." },
          { name: "Answer", value: answer },
        ],
      },
    };
  }

  if (lower.startsWith("!poll ")) {
    const q = input.slice(6).trim();
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.accent,
        title: "📊 Poll",
        description: `**${q}**\n\n👍 Yes\n👎 No`,
        footer: "React with 👍 or 👎 to vote!",
      },
    };
  }

  if (lower.startsWith("!ban ")) {
    const user = input.slice(5).trim();
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.danger,
        title: "🔨 User Banned",
        description: `**${user}** has been banned from the server.`,
        footer: "Moderation action logged",
      },
    };
  }

  if (lower.startsWith("!kick ")) {
    const user = input.slice(6).trim();
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.mention,
        title: "👢 User Kicked",
        description: `**${user}** has been kicked from the server.`,
        footer: "Moderation action logged",
      },
    };
  }

  if (lower.startsWith("!warn ")) {
    const user = input.slice(6).trim();
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.mention,
        title: "⚠️ Warning Issued",
        description: `**${user}** has been warned. This is warning #1.`,
        footer: "3 warnings = auto-ban",
      },
    };
  }

  if (lower.startsWith("!clear ")) {
    const n = input.slice(7).trim();
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      content: `🧹 Cleared **${n}** messages from this channel.`,
    };
  }

  if (lower.startsWith("!weather ")) {
    const city = input.slice(9).trim();
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.accent,
        title: `🌤️ Weather in ${city}`,
        fields: [
          { name: "Temperature", value: `${Math.floor(Math.random() * 30 + 10)}°C` },
          { name: "Condition", value: "Partly Cloudy ⛅" },
          { name: "Humidity", value: `${Math.floor(Math.random() * 40 + 40)}%` },
          { name: "Wind", value: `${Math.floor(Math.random() * 20 + 5)} km/h` },
        ],
      },
    };
  }

  if (lower.startsWith("!remind ")) {
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      embed: {
        color: DISCORD_COLORS.success,
        title: "⏰ Reminder Set!",
        description: `I'll remind you about: **${input.slice(8).trim()}**`,
        footer: "You'll receive a DM when the time comes.",
      },
    };
  }

  if (lower.startsWith("!volume ")) {
    const vol = parseInt(input.slice(8)) || 50;
    const clamped = Math.min(100, Math.max(0, vol));
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      content: `🔊 Volume set to **${clamped}%**`,
    };
  }

  if (lower === "!avatar") {
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      content: "🖼️ Here's your avatar! *(Avatar display coming soon — use !avatar @user in a real server)*",
    };
  }

  if (lower.startsWith("!")) {
    return {
      id: Date.now(), author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: ts(),
      content: `❓ Unknown command. Use \`!help\` to see all available commands.`,
    };
  }

  return null;
}

const initialMessages = [
  {
    id: 1, author: "Luna Bot", isBot: true, avatar: "🌙", timestamp: "Today at 12:00 PM",
    embed: {
      color: DISCORD_COLORS.luna,
      title: "🌙 Luna Bot is online!",
      description: "Hello! I'm **Luna**, your all-in-one Discord bot. Type `!help` to see what I can do!",
      fields: [
        { name: "Version", value: "v2.4.1" },
        { name: "Commands", value: `${LUNA_COMMANDS.length} total` },
        { name: "Prefix", value: "`!`" },
      ],
      footer: "Luna Bot • Always online 💜",
    },
  },
  {
    id: 2, author: "ServerOwner", isBot: false, avatar: "👑", timestamp: "Today at 12:01 PM",
    content: "Welcome everyone! Luna Bot is now set up in this server. Feel free to use !help to explore all features.",
  },
];

export default function LunaBotApp() {
  const [activeServer, setActiveServer] = useState(1);
  const [activeChannel, setActiveChannel] = useState(1);
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState("");
  const [showSidebar, setShowSidebar] = useState(true);
  const [activeTab, setActiveTab] = useState("chat");
  const [musicPlaying, setMusicPlaying] = useState(false);
  const [volume, setVolume] = useState(75);
  const [commandSearch, setCommandSearch] = useState("");
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    if (!input.trim()) return;
    const ts = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    const userMsg = {
      id: Date.now(), author: "You", isBot: false, avatar: "😊", timestamp: ts, content: input,
    };
    const botReply = generateLunaResponse(input, messages);
    setMessages(prev => botReply ? [...prev, userMsg, { ...botReply, id: Date.now() + 1 }] : [...prev, userMsg]);
    setInput("");
  };

  const filteredCommands = LUNA_COMMANDS.filter(c =>
    c.name.toLowerCase().includes(commandSearch.toLowerCase()) ||
    c.desc.toLowerCase().includes(commandSearch.toLowerCase()) ||
    c.category.toLowerCase().includes(commandSearch.toLowerCase())
  );

  const categories = [...new Set(filteredCommands.map(c => c.category))];

  const catColors = { General: "#5865F2", Music: "#23A55A", Moderation: "#F23F43", Leveling: "#FFD700", Economy: "#F0B232", Utility: "#00BCD4", Fun: "#FF69B4" };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "'Whitney', 'Helvetica Neue', Helvetica, Arial, sans-serif", background: DISCORD_COLORS.bg, color: DISCORD_COLORS.text, overflow: "hidden", minHeight: 600 }}>
      {/* Server Bar */}
      <div style={{ width: 72, background: DISCORD_COLORS.serverBar, display: "flex", flexDirection: "column", alignItems: "center", padding: "12px 0", gap: 8, flexShrink: 0 }}>
        <div onClick={() => setActiveServer(0)} style={{ width: 48, height: 48, borderRadius: activeServer === 0 ? "30%" : "50%", background: DISCORD_COLORS.accent, display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", fontSize: 22, transition: "border-radius 0.2s", flexShrink: 0 }}>🌙</div>
        <div style={{ width: 32, height: 2, background: DISCORD_COLORS.divider, borderRadius: 1 }} />
        {SERVERS.map(s => (
          <div key={s.id} style={{ position: "relative" }}>
            <div onClick={() => setActiveServer(s.id)} style={{ width: 48, height: 48, borderRadius: activeServer === s.id ? "30%" : "50%", background: activeServer === s.id ? DISCORD_COLORS.accent : DISCORD_COLORS.header, display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", fontSize: 20, transition: "all 0.15s", flexShrink: 0 }}>{s.icon}</div>
            {s.notifications > 0 && (
              <div style={{ position: "absolute", bottom: -2, right: -2, background: DISCORD_COLORS.danger, borderRadius: 10, minWidth: 16, height: 16, fontSize: 10, fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", padding: "0 4px", border: `2px solid ${DISCORD_COLORS.serverBar}` }}>
                {s.notifications > 9 ? "9+" : s.notifications}
              </div>
            )}
          </div>
        ))}
        <div style={{ width: 48, height: 48, borderRadius: "50%", background: DISCORD_COLORS.header, display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", fontSize: 24, color: DISCORD_COLORS.success, marginTop: "auto" }}>+</div>
      </div>

      {/* Channel Sidebar */}
      {showSidebar && (
        <div style={{ width: 240, background: DISCORD_COLORS.sidebar, display: "flex", flexDirection: "column", flexShrink: 0 }}>
          <div style={{ padding: "16px", borderBottom: `1px solid ${DISCORD_COLORS.divider}`, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <span style={{ fontWeight: 700, fontSize: 15 }}>{SERVERS.find(s => s.id === activeServer)?.name || "Luna Bot"}</span>
            <span style={{ color: DISCORD_COLORS.muted, cursor: "pointer", fontSize: 18 }}>⚙</span>
          </div>
          <div style={{ flex: 1, overflowY: "auto", padding: "8px 8px" }}>
            {/* Nav Tabs */}
            <div style={{ display: "flex", gap: 4, marginBottom: 12 }}>
              {["chat", "commands", "music"].map(tab => (
                <button key={tab} onClick={() => setActiveTab(tab)} style={{ flex: 1, padding: "6px 4px", background: activeTab === tab ? DISCORD_COLORS.accent : "transparent", border: "none", borderRadius: 4, color: activeTab === tab ? "#fff" : DISCORD_COLORS.muted, fontSize: 11, cursor: "pointer", fontWeight: activeTab === tab ? 600 : 400, transition: "all 0.15s", textTransform: "capitalize" }}>
                  {tab === "chat" ? "💬" : tab === "commands" ? "📋" : "🎵"}
                </button>
              ))}
            </div>

            {activeTab === "chat" && (
              <>
                {["TEXT CHANNELS", "MUSIC", "VOICE CHANNELS"].map(cat => {
                  const chans = CHANNELS.filter(c => c.category === cat);
                  if (!chans.length) return null;
                  return (
                    <div key={cat} style={{ marginBottom: 8 }}>
                      <div style={{ fontSize: 11, fontWeight: 700, color: DISCORD_COLORS.muted, padding: "4px 8px", textTransform: "uppercase", letterSpacing: 1 }}>{cat}</div>
                      {chans.map(ch => (
                        <div key={ch.id} onClick={() => ch.type === "text" && setActiveChannel(ch.id)} style={{ display: "flex", alignItems: "center", gap: 8, padding: "6px 8px", borderRadius: 4, cursor: ch.type === "text" ? "pointer" : "default", background: activeChannel === ch.id && ch.type === "text" ? DISCORD_COLORS.channelBg : "transparent", color: activeChannel === ch.id && ch.type === "text" ? DISCORD_COLORS.text : DISCORD_COLORS.muted, transition: "all 0.1s" }}>
                          <span style={{ fontSize: 16 }}>{ch.type === "text" ? "#" : "🔊"}</span>
                          <span style={{ fontSize: 14 }}>{ch.name}</span>
                          {ch.id === 1 && <span style={{ marginLeft: "auto", background: DISCORD_COLORS.danger, color: "#fff", borderRadius: 10, fontSize: 10, padding: "1px 6px", fontWeight: 700 }}>2</span>}
                        </div>
                      ))}
                    </div>
                  );
                })}
              </>
            )}

            {activeTab === "commands" && (
              <div>
                <input value={commandSearch} onChange={e => setCommandSearch(e.target.value)} placeholder="Search commands..." style={{ width: "100%", background: DISCORD_COLORS.bg, border: "none", borderRadius: 4, padding: "6px 8px", color: DISCORD_COLORS.text, fontSize: 13, marginBottom: 8, outline: "none", boxSizing: "border-box" }} />
                <div style={{ fontSize: 12, color: DISCORD_COLORS.muted, marginBottom: 4 }}>{filteredCommands.length} commands</div>
                {categories.map(cat => (
                  <div key={cat} style={{ marginBottom: 8 }}>
                    <div style={{ fontSize: 10, fontWeight: 700, color: catColors[cat] || DISCORD_COLORS.muted, padding: "2px 0", textTransform: "uppercase", letterSpacing: 1 }}>{cat}</div>
                    {filteredCommands.filter(c => c.category === cat).map(cmd => (
                      <div key={cmd.name} onClick={() => setInput(cmd.name.includes("<") ? cmd.name.split(" ")[0] + " " : cmd.name)} style={{ padding: "4px 6px", borderRadius: 4, cursor: "pointer", marginBottom: 2 }}>
                        <div style={{ fontSize: 12, fontWeight: 600, color: DISCORD_COLORS.luna, fontFamily: "monospace" }}>{cmd.name}</div>
                        <div style={{ fontSize: 11, color: DISCORD_COLORS.muted }}>{cmd.desc}</div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            )}

            {activeTab === "music" && (
              <div>
                <div style={{ background: DISCORD_COLORS.bg, borderRadius: 8, padding: 12, marginBottom: 8 }}>
                  <div style={{ fontSize: 11, color: DISCORD_COLORS.muted, marginBottom: 4 }}>NOW PLAYING</div>
                  <div style={{ fontSize: 14, fontWeight: 600, color: DISCORD_COLORS.text }}>{musicPlaying ? "Lo-fi Chill Mix" : "Nothing playing"}</div>
                  {musicPlaying && <div style={{ fontSize: 12, color: DISCORD_COLORS.muted }}>3:42 total</div>}
                  <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
                    <button onClick={() => setMusicPlaying(!musicPlaying)} style={{ flex: 1, background: musicPlaying ? DISCORD_COLORS.danger : DISCORD_COLORS.success, border: "none", borderRadius: 4, padding: "6px", color: "#fff", cursor: "pointer", fontSize: 12 }}>
                      {musicPlaying ? "⏸ Pause" : "▶ Play"}
                    </button>
                    <button onClick={() => setMusicPlaying(false)} style={{ flex: 1, background: DISCORD_COLORS.header, border: "none", borderRadius: 4, padding: "6px", color: DISCORD_COLORS.text, cursor: "pointer", fontSize: 12 }}>⏭ Skip</button>
                  </div>
                </div>
                <div style={{ background: DISCORD_COLORS.bg, borderRadius: 8, padding: 12, marginBottom: 8 }}>
                  <div style={{ fontSize: 11, color: DISCORD_COLORS.muted, marginBottom: 8 }}>VOLUME: {volume}%</div>
                  <input type="range" min="0" max="100" value={volume} onChange={e => setVolume(e.target.value)} style={{ width: "100%", accentColor: DISCORD_COLORS.luna }} />
                </div>
                <div style={{ background: DISCORD_COLORS.bg, borderRadius: 8, padding: 12 }}>
                  <div style={{ fontSize: 11, color: DISCORD_COLORS.muted, marginBottom: 8 }}>QUEUE</div>
                  {["Lo-fi Chill Mix", "Midnight Vibes", "Chill Hop Beats"].map((song, i) => (
                    <div key={i} style={{ display: "flex", gap: 8, padding: "4px 0", fontSize: 12 }}>
                      <span style={{ color: DISCORD_COLORS.muted }}>{i + 1}.</span>
                      <span>{song}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* User panel */}
          <div style={{ padding: "8px", background: DISCORD_COLORS.serverBar, display: "flex", alignItems: "center", gap: 8 }}>
            <div style={{ width: 32, height: 32, borderRadius: "50%", background: DISCORD_COLORS.accent, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, position: "relative" }}>
              😊
              <div style={{ position: "absolute", bottom: -1, right: -1, width: 10, height: 10, borderRadius: "50%", background: DISCORD_COLORS.online, border: `2px solid ${DISCORD_COLORS.serverBar}` }} />
            </div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: 13, fontWeight: 600 }}>You</div>
              <div style={{ fontSize: 11, color: DISCORD_COLORS.muted }}>#0000</div>
            </div>
            <span style={{ fontSize: 18, cursor: "pointer", color: DISCORD_COLORS.muted }}>🎙</span>
            <span style={{ fontSize: 18, cursor: "pointer", color: DISCORD_COLORS.muted }}>⚙</span>
          </div>
        </div>
      )}

      {/* Main Area */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", minWidth: 0 }}>
        {/* Header */}
        <div style={{ height: 48, background: DISCORD_COLORS.header, borderBottom: `1px solid ${DISCORD_COLORS.divider}`, display: "flex", alignItems: "center", padding: "0 16px", gap: 12, flexShrink: 0 }}>
          <button onClick={() => setShowSidebar(!showSidebar)} style={{ background: "none", border: "none", color: DISCORD_COLORS.muted, cursor: "pointer", fontSize: 20, padding: 0 }}>☰</button>
          <span style={{ color: DISCORD_COLORS.muted, fontSize: 20 }}>#</span>
          <span style={{ fontWeight: 700, fontSize: 15 }}>{CHANNELS.find(c => c.id === activeChannel)?.name || "general"}</span>
          <div style={{ height: 24, width: 1, background: DISCORD_COLORS.divider }} />
          <span style={{ color: DISCORD_COLORS.muted, fontSize: 13 }}>Luna Bot's command hub — type !help to start</span>
          <div style={{ marginLeft: "auto", display: "flex", gap: 16, color: DISCORD_COLORS.muted, fontSize: 20 }}>
            <span style={{ cursor: "pointer" }}>🔔</span>
            <span style={{ cursor: "pointer" }}>📌</span>
            <span style={{ cursor: "pointer" }}>🔍</span>
          </div>
        </div>

        {/* Messages */}
        <div style={{ flex: 1, overflowY: "auto", padding: "16px 16px 0", display: "flex", flexDirection: "column", gap: 4 }}>
          <div style={{ textAlign: "center", padding: "24px 0 16px" }}>
            <div style={{ fontSize: 48, marginBottom: 8 }}>🌙</div>
            <div style={{ fontWeight: 700, fontSize: 20 }}>Welcome to #general</div>
            <div style={{ color: DISCORD_COLORS.muted, fontSize: 13 }}>This is the beginning of the channel. Try typing <code style={{ background: DISCORD_COLORS.inputBg, padding: "1px 4px", borderRadius: 3 }}>!help</code></div>
          </div>
          {messages.map((msg, idx) => {
            const prev = messages[idx - 1];
            const sameAuthor = prev && prev.author === msg.author && !msg.embed;
            return (
              <div key={msg.id} style={{ display: "flex", gap: 16, padding: sameAuthor ? "1px 0 1px 72px" : "8px 0 1px", position: "relative" }}>
                {!sameAuthor && (
                  <div style={{ width: 40, height: 40, borderRadius: "50%", background: msg.isBot ? "rgba(124,111,247,0.2)" : DISCORD_COLORS.header, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 22, flexShrink: 0, border: msg.isBot ? `2px solid ${DISCORD_COLORS.luna}` : "none" }}>
                    {msg.avatar}
                  </div>
                )}
                <div style={{ flex: 1, minWidth: 0 }}>
                  {!sameAuthor && (
                    <div style={{ display: "flex", alignItems: "baseline", gap: 8, marginBottom: 2 }}>
                      <span style={{ fontWeight: 600, color: msg.isBot ? DISCORD_COLORS.lunaGlow : DISCORD_COLORS.text, fontSize: 14 }}>{msg.author}</span>
                      {msg.isBot && <span style={{ background: DISCORD_COLORS.accent, color: "#fff", fontSize: 10, padding: "1px 5px", borderRadius: 3, fontWeight: 600 }}>BOT</span>}
                      <span style={{ color: DISCORD_COLORS.muted, fontSize: 11 }}>{msg.timestamp}</span>
                    </div>
                  )}
                  {msg.content && <div style={{ fontSize: 14, lineHeight: 1.5, wordBreak: "break-word" }}>{msg.content}</div>}
                  {msg.embed && (
                    <div style={{ background: DISCORD_COLORS.cardBg, borderLeft: `4px solid ${msg.embed.color}`, borderRadius: "0 4px 4px 0", padding: "10px 12px", marginTop: 4, maxWidth: 440 }}>
                      {msg.embed.title && <div style={{ fontWeight: 700, fontSize: 14, color: DISCORD_COLORS.text, marginBottom: 6 }}>{msg.embed.title}</div>}
                      {msg.embed.description && <div style={{ fontSize: 13, color: DISCORD_COLORS.text, lineHeight: 1.5, marginBottom: msg.embed.fields ? 8 : 0, whiteSpace: "pre-line" }}>{msg.embed.description}</div>}
                      {msg.embed.fields && (
                        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(120px, 1fr))", gap: 8, marginTop: 4 }}>
                          {msg.embed.fields.map((f, i) => (
                            <div key={i}>
                              <div style={{ fontSize: 11, fontWeight: 700, color: DISCORD_COLORS.muted, textTransform: "uppercase", letterSpacing: 0.5 }}>{f.name}</div>
                              <div style={{ fontSize: 13, color: DISCORD_COLORS.text, marginTop: 2 }}>{f.value}</div>
                            </div>
                          ))}
                        </div>
                      )}
                      {msg.embed.footer && <div style={{ fontSize: 11, color: DISCORD_COLORS.muted, marginTop: 8, borderTop: `1px solid ${DISCORD_COLORS.divider}`, paddingTop: 6 }}>{msg.embed.footer}</div>}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div style={{ padding: "0 16px 24px", flexShrink: 0 }}>
          <div style={{ background: DISCORD_COLORS.inputBg, borderRadius: 8, display: "flex", alignItems: "center", padding: "0 16px", gap: 8 }}>
            <span style={{ color: DISCORD_COLORS.muted, fontSize: 22, cursor: "pointer" }}>+</span>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === "Enter" && sendMessage()}
              placeholder={`Message #${CHANNELS.find(c => c.id === activeChannel)?.name || "general"}`}
              style={{ flex: 1, background: "none", border: "none", outline: "none", color: DISCORD_COLORS.text, fontSize: 15, padding: "14px 0", caretColor: DISCORD_COLORS.text }}
            />
            <span style={{ color: DISCORD_COLORS.muted, fontSize: 22, cursor: "pointer" }}>😊</span>
            <span style={{ color: DISCORD_COLORS.muted, fontSize: 22, cursor: "pointer" }}>🎁</span>
            <button onClick={sendMessage} style={{ background: input.trim() ? DISCORD_COLORS.accent : "transparent", border: "none", borderRadius: 4, color: input.trim() ? "#fff" : DISCORD_COLORS.muted, cursor: input.trim() ? "pointer" : "default", padding: "6px 10px", fontSize: 18, transition: "all 0.15s" }}>➤</button>
          </div>
        </div>
      </div>

      {/* Members Sidebar */}
      <div style={{ width: 240, background: DISCORD_COLORS.sidebar, padding: "16px 8px", overflowY: "auto", flexShrink: 0 }}>
        <div style={{ fontSize: 11, fontWeight: 700, color: DISCORD_COLORS.muted, padding: "4px 8px", textTransform: "uppercase", letterSpacing: 1, marginBottom: 4 }}>Online — {MEMBERS.filter(m => m.status !== "offline").length}</div>
        {MEMBERS.filter(m => m.status !== "offline").map(member => (
          <div key={member.id} style={{ display: "flex", alignItems: "center", gap: 10, padding: "6px 8px", borderRadius: 4, cursor: "pointer", marginBottom: 2 }}>
            <div style={{ position: "relative", flexShrink: 0 }}>
              <div style={{ width: 32, height: 32, borderRadius: "50%", background: member.isBot ? "rgba(124,111,247,0.15)" : DISCORD_COLORS.header, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, border: member.isBot ? `2px solid ${DISCORD_COLORS.luna}` : "none" }}>
                {member.isBot ? "🌙" : member.name[0]}
              </div>
              <div style={{ position: "absolute", bottom: -1, right: -1, width: 10, height: 10, borderRadius: "50%", background: DISCORD_COLORS[member.status], border: `2px solid ${DISCORD_COLORS.sidebar}` }} />
            </div>
            <div style={{ minWidth: 0 }}>
              <div style={{ fontSize: 13, fontWeight: 500, color: member.color, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {member.name}
                {member.isBot && <span style={{ background: DISCORD_COLORS.accent, color: "#fff", fontSize: 9, padding: "0 4px", borderRadius: 2, marginLeft: 4, fontWeight: 700 }}>BOT</span>}
              </div>
              <div style={{ fontSize: 11, color: DISCORD_COLORS.muted }}>{member.role}</div>
            </div>
          </div>
        ))}
        <div style={{ fontSize: 11, fontWeight: 700, color: DISCORD_COLORS.muted, padding: "8px 8px 4px", textTransform: "uppercase", letterSpacing: 1 }}>Offline — {MEMBERS.filter(m => m.status === "offline").length}</div>
        {MEMBERS.filter(m => m.status === "offline").map(member => (
          <div key={member.id} style={{ display: "flex", alignItems: "center", gap: 10, padding: "6px 8px", borderRadius: 4, cursor: "pointer", opacity: 0.5 }}>
            <div style={{ width: 32, height: 32, borderRadius: "50%", background: DISCORD_COLORS.header, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 }}>
              {member.name[0]}
            </div>
            <div>
              <div style={{ fontSize: 13, fontWeight: 500 }}>{member.name}</div>
              <div style={{ fontSize: 11, color: DISCORD_COLORS.muted }}>{member.role}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
