Object.defineProperty(exports, "__esModule", { value: true });
exports.displayExperimentalSpaAlert = exports.displayDeployPreviewAlert = void 0;
var tslib_1 = require("tslib");
var alertActions_1 = tslib_1.__importDefault(require("app/actions/alertActions"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
function displayDeployPreviewAlert() {
    if (!constants_1.DEPLOY_PREVIEW_CONFIG) {
        return;
    }
    var branch = constants_1.DEPLOY_PREVIEW_CONFIG.branch, commitSha = constants_1.DEPLOY_PREVIEW_CONFIG.commitSha, githubOrg = constants_1.DEPLOY_PREVIEW_CONFIG.githubOrg, githubRepo = constants_1.DEPLOY_PREVIEW_CONFIG.githubRepo;
    var repoUrl = "https://github.com/" + githubOrg + "/" + githubRepo;
    var commitLink = (<externalLink_1.default href={repoUrl + "/commit/" + commitSha}>
      {locale_1.t('%s@%s', githubOrg + "/" + githubRepo, commitSha.slice(0, 6))}
    </externalLink_1.default>);
    var branchLink = (<externalLink_1.default href={repoUrl + "/tree/" + branch}>{branch}</externalLink_1.default>);
    alertActions_1.default.addAlert({
        id: 'deploy-preview',
        message: locale_1.tct('You are viewing a frontend deploy preview of [commitLink] ([branchLink])', { commitLink: commitLink, branchLink: branchLink }),
        type: 'warning',
        neverExpire: true,
        noDuplicates: true,
    });
}
exports.displayDeployPreviewAlert = displayDeployPreviewAlert;
function displayExperimentalSpaAlert() {
    if (!constants_1.EXPERIMENTAL_SPA) {
        return;
    }
    alertActions_1.default.addAlert({
        id: 'develop-proxy',
        message: locale_1.t('You are developing against production Sentry API, please BE CAREFUL, as your changes will affect production data.'),
        type: 'warning',
        neverExpire: true,
        noDuplicates: true,
    });
}
exports.displayExperimentalSpaAlert = displayExperimentalSpaAlert;
//# sourceMappingURL=deployPreview.jsx.map