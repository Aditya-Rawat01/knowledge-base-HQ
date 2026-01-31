import express, {
  type NextFunction,
  type Request,
  type Response,
} from "express";
import cookieParser from "cookie-parser";
const app = express();
app.use(express.json());
app.use(cookieParser("the-string-to-sign-cookies"));

type data = {
  userId: string;
  refreshToken: string | null;
};
// for simulation purposes
const database: data[] = [];

function createRefreshToken(userId: string) {
  // use better encryption algorithm here.
  // this is just to understand the concept.
  
  const refreshToken = userId + " " + crypto.randomUUID();

  return refreshToken;
}
function updateRefreshToken(userId: string, refreshToken: string) {
  for (let i = 0; i < database.length; i++) {
    if (database[i]!.userId == userId) {
      database[i]!.refreshToken = refreshToken;
    }
  }
  return;
}
function accessToken(req: Request, res: Response, next: NextFunction) {
  const cookies = req.signedCookies;
  if (!cookies["access-token"]) {
    if (!cookies["refresh-token"]) {
      return res.status(401).json({
        msg: "not authenticated, dude!",
      });
    } else {
      // check if the person is using old removed refresh token
      let userId = null;
      for (let i = 0; i < database.length; i++) {
        if (database[i]!.refreshToken == cookies["refresh-token"]) {
          userId = database[i]!.userId;
        }
      }
      // if userId stays null that means someone used old token, revoke all the refresh-tokens and redirect the user to login page whenever he comes.
      // else just updates the original refresh-token

      if (!userId) {
        // decrypt the refresh token to get the original user id.
        let originalUserId = cookies["refresh-token"].split(' ')[0]; // just for learning and demonstration!!!!
        for (let i = 0; i < database.length; i++) {
          if (database[i]!.userId == originalUserId) {
            database[i]!.refreshToken = null;
            // null is not a good value here, redirect to the login page.
            return res.json({
              msg: "old token found, redirecting to login and removing old refresh tokens",
            });
          }
        }
      } else {
        renewBothTokens(userId, res);
        next();
      }
    }
  } else {
    next();
  }
}
function renewBothTokens(userId: string, res: Response) {
  console.log(
    "access-token and refresh-token got renewed without the user knowing!"
  );

  // assigning a new refresh token so revoking old one and storing new one in the db.
  const refreshToken = createRefreshToken(userId);
  updateRefreshToken(userId, refreshToken);
  res.cookie("access-token", userId, {
    maxAge: 1000 * 60 * 1,
    httpOnly: true,
    secure: true,
    sameSite: true,
    signed: true,
  });
  res.cookie("refresh-token", refreshToken, {
    maxAge: 1000 * 60 * 2,
    httpOnly: true,
    secure: true,
    sameSite: true,
    signed: true,
  });
  return;
}
app.get("/signup", (req: Request, res: Response) => {
  const body = req.body;
  if (!body) {
    return res.json({
      msg: "no body",
    });
  }
  const userId = req.body.id;
  if (!userId) {
    return res.json({
      msg: "pass the user id",
    });
  }
  let exists = database.find((u) => u.userId === userId);
  if (exists) {
    return res.json({
      msg: "already signed up please sign in",
    });
  }
  let refreshToken = createRefreshToken(userId);
  res.cookie("access-token", userId, {
    maxAge: 1000 * 60 * 1,
    httpOnly: true,
    secure: true,
    sameSite: true,
    signed: true,
  });
  res.cookie("refresh-token", refreshToken, {
    maxAge: 1000 * 60 * 2,
    httpOnly: true,
    secure: true,
    sameSite: true,
    signed: true,
  });
  database.push({ userId, refreshToken });
  return res.json({
    msg: "hello new user",
    userId: userId,
  });
});

app.get("/login", (req: Request, res: Response) => {
  const body = req.body;
  if (!body) {
    return res.json({
      msg: "no body",
    });
  }
  const userId = req.body.id;
  if (!userId) {
    return res.json({
      msg: "pass the user id",
    });
  }
  let exists = database.find((u) => u.userId === userId);
  if (!exists) {
    return res.json({
      msg: "user doesn't exist",
    });
  }
  const refreshToken = createRefreshToken(userId);
  res.cookie("access-token", userId, {
    maxAge: 1000 * 60 * 1,
    httpOnly: true,
    secure: true,
    sameSite: true,
    signed: true,
  });
  res.cookie("refresh-token", refreshToken, {
    maxAge: 1000 * 60 * 2,
    httpOnly: true,
    secure: true,
    sameSite: true,
    signed: true,
  });

  updateRefreshToken(userId, refreshToken);
  return res.json({
    msg: "hello old user",
    userId: userId,
  });
});

app.get("/authenticated", accessToken, (req, res) => {
  return res.json({
    msg: "hello authenticated user",
  });
});

app.listen(3000, () => {
  console.log("token rotation server started!");
});
