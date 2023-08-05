Object.defineProperty(exports, "__esModule", { value: true });
exports.ICON_PATHS = exports.DEFAULT_ICON = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var logo_amixr_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-amixr.svg"));
var logo_asana_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-asana.svg"));
var logo_asayer_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-asayer.svg"));
var logo_aws_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-aws.svg"));
var logo_azure_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-azure.svg"));
var logo_bitbucket_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-bitbucket.svg"));
var logo_bitbucket_server_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-bitbucket-server.svg"));
var logo_calixa_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-calixa.svg"));
var logo_campfire_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-campfire.svg"));
var logo_clickup_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-clickup.svg"));
var logo_clubhouse_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-clubhouse.svg"));
var logo_datadog_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-datadog.svg"));
var logo_default_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-default.svg"));
var logo_flowdock_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-flowdock.svg"));
var logo_fullstory_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-fullstory.svg"));
var logo_github_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-github.svg"));
var logo_github_actions_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-github-actions.svg"));
var logo_github_enterprise_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-github-enterprise.svg"));
var logo_gitlab_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-gitlab.svg"));
var logo_heroku_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-heroku.svg"));
var logo_jira_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-jira.svg"));
var logo_jira_server_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-jira-server.svg"));
var logo_komodor_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-komodor.svg"));
var logo_lighthouse_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-lighthouse.svg"));
var logo_linear_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-linear.svg"));
var logo_msteams_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-msteams.svg"));
var logo_netlify_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-netlify.svg"));
var logo_octohook_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-octohook.svg"));
var logo_opsgenie_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-opsgenie.svg"));
var logo_pagerduty_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-pagerduty.svg"));
var logo_phabricator_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-phabricator.svg"));
var logo_pivotaltracker_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-pivotaltracker.svg"));
var logo_pushover_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-pushover.svg"));
var logo_quill_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-quill.svg"));
var logo_redmine_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-redmine.svg"));
var logo_rocketchat_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-rocketchat.svg"));
var logo_rookout_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-rookout.svg"));
var logo_segment_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-segment.svg"));
var logo_sentry_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-sentry.svg"));
var logo_slack_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-slack.svg"));
var logo_spikesh_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-spikesh.svg"));
var logo_split_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-split.svg"));
var logo_taiga_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-taiga.svg"));
var logo_teamwork_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-teamwork.svg"));
var logo_trello_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-trello.svg"));
var logo_twilio_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-twilio.svg"));
var logo_vercel_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-vercel.svg"));
var logo_victorops_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-victorops.svg"));
var logo_visualstudio_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-visualstudio.svg"));
var logo_youtrack_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-youtrack.svg"));
var logo_zepel_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-zepel.svg"));
var logo_zulip_svg_1 = tslib_1.__importDefault(require("sentry-logos/logo-zulip.svg"));
// Map of plugin id -> logo filename
exports.DEFAULT_ICON = logo_default_svg_1.default;
exports.ICON_PATHS = {
    _default: exports.DEFAULT_ICON,
    sentry: logo_sentry_svg_1.default,
    browsers: logo_sentry_svg_1.default,
    device: logo_sentry_svg_1.default,
    interface_types: logo_sentry_svg_1.default,
    os: logo_sentry_svg_1.default,
    urls: logo_sentry_svg_1.default,
    webhooks: logo_sentry_svg_1.default,
    'amazon-sqs': logo_aws_svg_1.default,
    aws_lambda: logo_aws_svg_1.default,
    amixr: logo_amixr_svg_1.default,
    asana: logo_asana_svg_1.default,
    asayer: logo_asayer_svg_1.default,
    bitbucket: logo_bitbucket_svg_1.default,
    bitbucket_pipelines: logo_bitbucket_svg_1.default,
    bitbucket_server: logo_bitbucket_server_svg_1.default,
    calixa: logo_calixa_svg_1.default,
    campfire: logo_campfire_svg_1.default,
    clickup: logo_clickup_svg_1.default,
    clubhouse: logo_clubhouse_svg_1.default,
    datadog: logo_datadog_svg_1.default,
    flowdock: logo_flowdock_svg_1.default,
    fullstory: logo_fullstory_svg_1.default,
    github: logo_github_svg_1.default,
    github_actions: logo_github_actions_svg_1.default,
    github_enterprise: logo_github_enterprise_svg_1.default,
    gitlab: logo_gitlab_svg_1.default,
    heroku: logo_heroku_svg_1.default,
    jira: logo_jira_svg_1.default,
    'jira-atlassian-connect': logo_jira_svg_1.default,
    'jira-ac': logo_jira_svg_1.default,
    jira_server: logo_jira_server_svg_1.default,
    komodor: logo_komodor_svg_1.default,
    lighthouse: logo_lighthouse_svg_1.default,
    linear: logo_linear_svg_1.default,
    msteams: logo_msteams_svg_1.default,
    netlify: logo_netlify_svg_1.default,
    octohook: logo_octohook_svg_1.default,
    opsgenie: logo_opsgenie_svg_1.default,
    pagerduty: logo_pagerduty_svg_1.default,
    phabricator: logo_phabricator_svg_1.default,
    pivotal: logo_pivotaltracker_svg_1.default,
    pushover: logo_pushover_svg_1.default,
    quill: logo_quill_svg_1.default,
    redmine: logo_redmine_svg_1.default,
    rocketchat: logo_rocketchat_svg_1.default,
    rookout: logo_rookout_svg_1.default,
    segment: logo_segment_svg_1.default,
    slack: logo_slack_svg_1.default,
    spikesh: logo_spikesh_svg_1.default,
    split: logo_split_svg_1.default,
    taiga: logo_taiga_svg_1.default,
    teamwork: logo_teamwork_svg_1.default,
    trello: logo_trello_svg_1.default,
    twilio: logo_twilio_svg_1.default,
    visualstudio: logo_visualstudio_svg_1.default,
    vsts: logo_azure_svg_1.default,
    youtrack: logo_youtrack_svg_1.default,
    vercel: logo_vercel_svg_1.default,
    victorops: logo_victorops_svg_1.default,
    zepel: logo_zepel_svg_1.default,
    zulip: logo_zulip_svg_1.default,
};
var PluginIcon = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  height: ", "px;\n  width: ", "px;\n  border-radius: 2px;\n  border: 0;\n  display: inline-block;\n  background-size: contain;\n  background-position: center center;\n  background-repeat: no-repeat;\n  background-image: url(", ");\n"], ["\n  position: relative;\n  height: ", "px;\n  width: ", "px;\n  border-radius: 2px;\n  border: 0;\n  display: inline-block;\n  background-size: contain;\n  background-position: center center;\n  background-repeat: no-repeat;\n  background-image: url(", ");\n"])), function (p) { return p.size; }, function (p) { return p.size; }, function (_a) {
    var pluginId = _a.pluginId;
    return (pluginId !== undefined && exports.ICON_PATHS[pluginId]) || exports.DEFAULT_ICON;
});
PluginIcon.defaultProps = {
    pluginId: '_default',
    size: 20,
};
exports.default = PluginIcon;
var templateObject_1;
//# sourceMappingURL=pluginIcon.jsx.map