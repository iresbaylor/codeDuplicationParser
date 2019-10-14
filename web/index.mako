<!DOCTYPE html>
<html lang="en">

<%
    proj_name = "Cyclone"
    proj_brief = "Python 3 Code Clone Detector"
%>

<head>

    <meta charset="UTF-8">
    <title>${proj_name} - ${proj_brief}</title>

    <!--Let browser know website is optimized for mobile-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- Compiled and minified CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">

    <!--Import Google Icon Font-->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

</head>

<body>
    <div class="container">

        <div class="center-align">
            <h2 class="blue-text text-accent-4">
                ${proj_name}
            </h2>
            <div class="blue-text text-accent-2">
                ${proj_brief}
            </div>
        </div>

        <div class="row center-align">
            <form method="GET" class="col s6 offset-s3">
                <div class="row">
                    <div class="input-field col s12">
                        <input id="repo" name="repo" class="validate" type="text" required>
                        <label for="repo">Git repository</label>
                    </div>

                    <button class="btn blue accent-3 waves-effect waves-light" type="submit">
                        Analyze repository
                        <i class="material-icons right">send</i>
                    </button>
                </div>
            </form>
        </div>

        % if msg:
        <div class="row">
            <div class="col s12 center-align">
                <h4>
                    ${msg}
                </h4>
            </div>
        </div>
        % endif

        % if repos:
        <div class="row">
            <div class="col s6 offset-s3">
                <ul class="collection with-header">
                    <li class="collection-header">
                        <h4>
                            Matching repositories
                        </h4>
                    </li>

                    % for r in repos:
                    <li class="collection-item">
                        <h5><a href="?repo=https%3A%2F%2F${r.server}%2F${r.user}%2F${r.name}">${r.name}</a></h5>
                        <b>URL:</b> <a href="${r.url}">${r.url}</a><br>
                        <b>Server:</b> <a href="https://${r.server}">${r.server}</a><br>
                        <b>User:</b> <a href="https://${r.server}/${r.user}">${r.user}</a><br>
                        <b>Status:</b> ${r.status_desc or r.status_name}
                    </li>
                    % endfor

                </ul>
            </div>
        </div>
        % endif

        % if clones:
        <div class="row">
            <div class="col s8 offset-s2">
                <ul class="collection with-header">
                    <li class="collection-header">
                        <h4>
                            Detected clones
                        </h4>
                    </li>

                    % for c in clones:
                    <li class="collection-item">
                        <ul class="collection with-header">
                            <li class="collection-header">
                                <h5>
                                    ${c.value} - Weight: ${c.match_weight}
                                </h5>
                            </li>

                            % for o, s in c.origins.items():
                            <li class="collection-header">
                                ${o} - Similarity: ${format(s * 100, "g")} %
                            </li>
                            % endfor

                        </ul>
                    </li>
                    % endfor

                </ul>
            </div>
        </div>
        % endif

    </div>
</body>

<!-- Compiled and minified JavaScript -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>

</html>
