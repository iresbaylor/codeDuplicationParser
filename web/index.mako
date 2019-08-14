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

        % if result:
        <div class="row">
            <div class="col s8 offset-s2">
                <ul class="collection with-header">
                    <li class="collection-header">
                        <h4>
                            Detected clones
                        </h4>
                    </li>

                    % for c in result:
                    <li class="collection-item">
                        <ul class="collection with-header">
                            <li class="collection-header">
                                <h5>
                                    ${c.value} - Weight: ${c.weight}
                                </h5>
                            </li>

                            % for o in c.origins:
                            <li class="collection-header">
                                ${o[0]} - Similarity: ${format(o[1] * 100, "g")} %
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
