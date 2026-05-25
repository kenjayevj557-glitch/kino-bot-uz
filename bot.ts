import TelegramBot from "node-telegram-bot-api";
import { logger } from "./lib/logger";

const TELEGRAM_BOT_TOKEN = process.env["TELEGRAM_BOT_TOKEN"];
const OMDB_API_KEY = process.env["OMDB_API_KEY"];

interface OmdbMovie {
  Title: string;
  Year: string;
  Plot: string;
  Poster: string;
  imdbRating: string;
  Response: string;
  Error?: string;
}

interface OmdbSearchResult {
  Search?: Array<{ Title: string; Year: string; imdbID: string; Type: string }>;
  Response: string;
  Error?: string;
}

async function fetchMovie(title: string): Promise<OmdbMovie | null> {
  const url = `http://www.omdbapi.com/?t=${encodeURIComponent(title)}&apikey=${OMDB_API_KEY}`;
  logger.info({ url }, "Fetching movie from OMDb");
  const res = await fetch(url);
  if (!res.ok) return null;
  const data = (await res.json()) as OmdbMovie;
  if (data.Response === "False") return null;
  return data;
}

async function searchMovies(query: string): Promise<OmdbSearchResult> {
  const url = `http://www.omdbapi.com/?s=${encodeURIComponent(query)}&type=movie&apikey=${OMDB_API_KEY}`;
  const res = await fetch(url);
  const data = (await res.json()) as OmdbSearchResult;
  return data;
}

function escapeMd(text: string): string {
  return text.replace(/[_*[\]()~`>#+=|{}.!\-]/g, "\\$&");
}

function formatCaption(movie: OmdbMovie): string {
  const rating = movie.imdbRating !== "N/A" ? `${movie.imdbRating}/10` : "N/A";
  let caption = `🎬 *${escapeMd(movie.Title)}* (${movie.Year})\n\n`;
  caption += `⭐ IMDb: ${escapeMd(rating)}\n\n`;
  caption += `📖 ${escapeMd(movie.Plot)}`;
  return caption;
}

export function startBot(): void {
  if (!TELEGRAM_BOT_TOKEN) {
    logger.warn("TELEGRAM_BOT_TOKEN is not set — bot will not start");
    return;
  }
  if (!OMDB_API_KEY) {
    logger.warn("OMDB_API_KEY is not set — bot will not start");
    return;
  }

  const bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: true });
  logger.info("Telegram movie bot started");

  bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(
      chatId,
      `👋 Welcome to *Movie Search Bot*\!\n\nI can find any movie for you \-\- just use:\n\n🔍 */search \<movie title\>*\n\nExample: \`/search Inception\``,
      { parse_mode: "MarkdownV2" }
    );
  });

  bot.onText(/\/help/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(
      chatId,
      `*How to use Movie Search Bot:*\n\n• */search \<title\>* \-\- find a movie by name\n• */start* \-\- show welcome message\n• */help* \-\- show this help\n\nExample: \`/search The Dark Knight\``,
      { parse_mode: "MarkdownV2" }
    );
  });

  bot.onText(/\/search(?:\s+(.+))?/, async (msg, match) => {
    const chatId = msg.chat.id;
    const query = match?.[1]?.trim();

    if (!query) {
      await bot.sendMessage(
        chatId,
        "Please provide a movie title\. Example: \`/search Interstellar\`",
        { parse_mode: "MarkdownV2" }
      );
      return;
    }

    const searching = await bot.sendMessage(
      chatId,
      `🔍 Searching for *${escapeMd(query)}*\.\.\.`,
      { parse_mode: "MarkdownV2" }
    );

    try {
      const movie = await fetchMovie(query);

      if (!movie) {
        const results = await searchMovies(query);

        if (results.Response === "True" && results.Search && results.Search.length > 0) {
          const suggestions = results.Search.slice(0, 5)
            .map((m, i) => `${i + 1}\. *${escapeMd(m.Title)}* \(${m.Year}\)`)
            .join("\n");

          await bot.editMessageText(
            `❌ No exact match for "*${escapeMd(query)}*"\.\n\nDid you mean one of these?\n\n${suggestions}\n\nTry: \`/search \<exact title\>\``,
            { chat_id: chatId, message_id: searching.message_id, parse_mode: "MarkdownV2" }
          );
        } else {
          await bot.editMessageText(
            `❌ No movies found for "*${escapeMd(query)}*"\. Try a different title\.`,
            { chat_id: chatId, message_id: searching.message_id, parse_mode: "MarkdownV2" }
          );
        }
        return;
      }

      const caption = formatCaption(movie);
      await bot.deleteMessage(chatId, searching.message_id);

      if (movie.Poster && movie.Poster !== "N/A") {
        await bot.sendPhoto(chatId, movie.Poster, {
          caption,
          parse_mode: "MarkdownV2",
        });
      } else {
        await bot.sendMessage(chatId, caption, { parse_mode: "MarkdownV2" });
      }
    } catch (err) {
      logger.error({ err }, "Error fetching movie");
      await bot.editMessageText(
        "⚠️ Something went wrong while fetching movie data\. Please try again\.",
        { chat_id: chatId, message_id: searching.message_id, parse_mode: "MarkdownV2" }
      );
    }
  });

  bot.on("message", (msg) => {
    const chatId = msg.chat.id;
    const text = msg.text ?? "";
    if (!text.startsWith("/")) {
      bot.sendMessage(
        chatId,
        `Use */search \<movie title\>* to look up a movie\.\n\nExample: \`/search Parasite\``,
        { parse_mode: "MarkdownV2" }
      );
    }
  });

  bot.on("polling_error", (err) => {
    logger.error({ err }, "Telegram polling error");
  });
}
