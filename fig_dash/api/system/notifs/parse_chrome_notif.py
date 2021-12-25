#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /* read chrome's browser notifications. */
import getpass
notif_path = f"/home/{getpass.getuser()}/.config/google-chrome/Default/Platform Notifications/000003.log"


class ChromeNotifcation:
    def __init__(self, i, texts, urls):
        self.i = i
        self.texts = self.texts
        self.urls = urls

    def __str__(self):
        return "\n".join(urls) + "\n"join(texts)

    def  __eq__(self, other):
        return self.i == other.i

    def __lt__(self, other):
        return self.i < other.i

    def __gt__(self, other):
        return self.i > other.i


class ChromeNotificationHistoryReader:
    def __init__(self, path=notif_path):
        self.path = path
        self.notifs = self.parse(path)

    def parse_lines(self, path):
        pass

    def parse(self, path):
        notifs = []
        list_of_tokens = self.parse_lines(path)
        instance_counter = 0
        for token_list in list_of_tokens:
            urls = []
            texts = []
            for token in token_list:
                if token.startswith("https://") or token.startswith("http://"):
                    urls.add(token)
                else:
                    texts.add(token)
            # remove unimportant urls.
            # removes shorter url when it is contained completely in another url.

            # ret.add(new ChromeNotificationStuff(instanceCounter, urls, texts));
            instance_counter += 1
        notifs = sorted(notifs);
        
        return notifs



    final private static double MIN_LENGTH_DIFFERENCE_RATIO = 0.7;//0.9;
    final private static double MIN_REMAININGLINES_PERCENTAGEOF_ALLLINES = 0.2;




    final private static class DumbTokenList {


        final private static int MIN_LENGTH = 10; //6;
        final private static String[] EXTENSIONS = new String[] { ".jpg", ".jpeg", ".png", ".gif", ".html", ".htm", ".php" };
        final private static int MAX_EXTRA_CRAP_AFTER_EXTENSIONS = 3;
        final private static String SAFE_URL_CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;="; // https://stackoverflow.com/a/1547940/3500521

        final private String originalText;
        final private List<String> tokens;


        private DumbTokenList(final String textWithBinaryCrap) {

            originalText = textWithBinaryCrap;

            final List<String> tokens = new ArrayList<>();

            final Consumer<String> addTokenButTryToDecrappifyExtensionsFirstAnTing = token -> {


                if (token.startsWith("ttps://") || token.startsWith("ttp://")) {
                    token = "h" + token;
                }


                final List<String> newTokens = new ArrayList<>();

                if (token.startsWith("http")) {
                    final int tokenLength = token.length();
                    boolean found = false;
                    for (int i = 0; i < tokenLength; i++) {
                        final char c = token.charAt(i);
                        if (SAFE_URL_CHARACTERS.indexOf(c) < 0) {
                            newTokens.add(token.substring(0, i));
                            newTokens.add(token.substring(i));
                            found = true;
                            break;
                        }
                    }
                    if (!found) {
                        newTokens.add(token);
                    }
                } else {
                    newTokens.add(token);
                }

                for (String newToken : newTokens) {


                    String foundExt = null;
                    int foundExtLen = 0;
                    int foundExtAt = -1;
                    for (String extension : EXTENSIONS) {
                        final int idx = newToken.indexOf(extension);
                        if (idx >= 0) {
                            final int extLen = extension.length();
                            if (idx > foundExtAt || (idx == foundExtAt && extLen > foundExtLen)) {
                                foundExt = extension;
                                foundExtLen = extLen;
                                foundExtAt = idx;
                            }
                        }
                    }
                    if (foundExt != null) {
                        final int amountOfCharactersAfterThisFind = newToken.length() - foundExtAt - foundExtLen;
                        if (amountOfCharactersAfterThisFind <= MAX_EXTRA_CRAP_AFTER_EXTENSIONS) {
                            // OK. Shorten this bitch.
                            newToken = newToken.substring(0, foundExtAt + foundExtLen);
                        }
                    }


                    if (newToken.startsWith("http")) {
                        if (!newToken.startsWith("http://") && !newToken.startsWith("https://")) {
                            continue;
                        }
                    }


                    if (newToken.startsWith("/watch?v=")) {
                        newToken = "https://www.youtube.com" + newToken;
                    }


                    if (newToken.length() >= MIN_LENGTH) {
                        tokens.add(newToken);
                    }


                }

            };

            final StringBuilder sb = new StringBuilder();

            final int len = textWithBinaryCrap.length();
            for (int i = 0; i <= len + 1; i++) {

                final char c = i < len ? textWithBinaryCrap.charAt(i) : 0;

                if (c < ' ' || c == '"') {

                    String potentialText = sb.toString();
                    while (true) {
                        final int httpIDX = potentialText.indexOf("http", 1);
                        if (httpIDX < 0) {
                            addTokenButTryToDecrappifyExtensionsFirstAnTing.accept(potentialText);
                            break;
                        } else {
                            final String snippet = potentialText.substring(0, httpIDX);
                            potentialText = potentialText.substring(httpIDX);
                            addTokenButTryToDecrappifyExtensionsFirstAnTing.accept(snippet);
                        }
                    }

                    sb.setLength(0);

                    if (c == '"') {
                        // Skip this and the next. (thus "i < len +1")
                        i++;
                    }
                } else {
                    sb.append(c);
                }
            }


            // Remove quasi-duplicates. Sue me.
            //            System.err.println("\n*** STARTING DEDUPLICATION ***");
            final int lSize = tokens.size();
            for (int i = lSize - 1; i > 0; i--) { // (not 0 itself, wouldn't make sense)

                if (i < tokens.size()) {

                    final String entry = tokens.get(i);

                    for (int ii = i - 1; ii >= 0; ii--) { // (incl. 0)

                        final String otherEntry = tokens.get(ii);

                        final Boolean removeNoneOrFirstOrSecond = areLinesTooSimilar(entry, otherEntry);
                        if (removeNoneOrFirstOrSecond != null) {

                            if (!removeNoneOrFirstOrSecond) {
                                final String removed = tokens.remove(i);
                                //                                System.err.println("\nREMOVED: " + removed + "\nKEPT   : " + otherEntry); // because was better or equal
                            } else {
                                final String removed = tokens.remove(ii);
                                //                                System.err.println("\nREMOVED: " + removed + "\nKEPT   : " + entry); // because was better or equal
                            }
                            break; // IMPORTANT!
                        }

                    }
                }
            }


            this.tokens = Collections.unmodifiableList(tokens);

        }


        public String toString() {

            final StringBuilder sb = new StringBuilder();
            for (String token : tokens) {
                sb.append(token).append('\n');
            }
            return sb.toString();
        }


    }    
    #  * Do NOT call with NULL/EMPTY arguments.
    #  *
    #  * @return NULL if not too similar. False if the FIRST seems superfluous. True if the SECOND seems superfluous.
    #  */
    private static Boolean areLinesTooSimilar(final String line1,
                                              final String line2) {

        final int l1 = line1.length();
        final int l2 = line2.length();

        final double lenDiffRatio = Math.min(l1, l2) / (double) Math.max(l1, l2); // Results in 1 or less.

        if (lenDiffRatio >= MIN_LENGTH_DIFFERENCE_RATIO) {

            if (l2 < l1) {
                // Compare the other way round.
                if (line1.contains(line2)) {
                    return false;
                }
            } else {
                if (line2.contains(line1)) {
                    return true;
                }
            }

        }

        return null;
    }


    private static List<DumbTokenList> doTheInsaneParsingThing(final File file) {

        final List<DumbTokenList> ret = new ArrayList<>();

        final StringBuilder sb = new StringBuilder();
        try (final InputStream is = new BufferedInputStream(new FileInputStream(file))) {

            final int bufMinus1 = 4;
            final Charset charset = Charset.forName("Cp1252"); // =ansi

            final int[] buf = new int[bufMinus1 + 1]; // "DATA"
            //            while ((buf[buf.length - 1] = is.read()) >= 0) {
            while (true) {

                buf[bufMinus1] = is.read();

                if (buf[bufMinus1] < 0 || (
                        buf[0] == 'D' &&
                                buf[1] == 'A' &&
                                buf[2] == 'T' &&
                                buf[3] == 'A' &&
                                buf[4] == ':')) {

                    if (sb.length() > 0) {
                        ret.add(new DumbTokenList(sb.toString()));
                        sb.setLength(0);
                    }

                    if (buf[bufMinus1] < 0) {
                        break;
                    }

                } else {

                    sb.append(new String(new byte[] { (byte) buf[bufMinus1] }, charset));
                    //                    sb.append((char) buf[bufMinus1]);
                }


                // Shift minibuffer to front.
                for (int i = 0; i < bufMinus1; i++) {
                    buf[i] = buf[i + 1];
                }
            }


        } catch (IOException e) {
            e.printStackTrace();
        }


        // DEDUPLICATE DTLs
        for (int i = ret.size() - 1; i > 0; i--) {

            if (i < ret.size()) {
                final DumbTokenList dtlThis = ret.get(i);
                final int dtlThisTokenCount = dtlThis.tokens.size();

                for (int ii = i - 1; ii >= 0; ii--) {
                    final DumbTokenList dtlThat = ret.get(ii);
                    final int dtlThatTokenCount = dtlThat.tokens.size();


                    int scoreViaRemainingLines_this = dtlThisTokenCount;
                    int scoreViaRemainingLines_that = dtlThatTokenCount;


                    for (int o = 0; o < dtlThisTokenCount; o++) {
                        final String tokenThis = dtlThis.tokens.get(o);
                        for (int oo = 0; oo < dtlThatTokenCount; oo++) {
                            final String tokenThat = dtlThat.tokens.get(oo);

                            final Boolean tooSimilar = areLinesTooSimilar(tokenThis, tokenThat);
                            if (tooSimilar != null) {
                                scoreViaRemainingLines_this--;
                                scoreViaRemainingLines_that--;
                                break;
                            }

                        }
                    }

                    if (scoreViaRemainingLines_this < 0 || scoreViaRemainingLines_that < 0) {
                        throw new Error();
                    }

                    final double scoreActual_this = scoreViaRemainingLines_this / (double) dtlThisTokenCount;
                    final double scoreActual_that = scoreViaRemainingLines_that / (double) dtlThatTokenCount;


                    if (scoreViaRemainingLines_this < scoreViaRemainingLines_that) {
                        if (scoreActual_this < MIN_REMAININGLINES_PERCENTAGEOF_ALLLINES) {
                            final DumbTokenList removed = ret.remove(i);
                            //                            System.err.println("\nREMOVED:\n" + removed + "\nKEPT   :\n" + dtlThat);
                            break; // IMPORTANT.
                        }
                    } else {
                        if (scoreActual_that < MIN_REMAININGLINES_PERCENTAGEOF_ALLLINES) {
                            final DumbTokenList removed = ret.remove(ii);
                            //                            System.err.println("\nREMOVED:\n" + removed + "\nKEPT   :\n" + dtlThis);
                            break; // IMPORTANT.
                        }
                    }


                }

            }
        }

        return ret;
    }


}