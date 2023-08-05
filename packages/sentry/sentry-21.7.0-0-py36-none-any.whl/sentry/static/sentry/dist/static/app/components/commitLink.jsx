Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
// TODO(epurkhiser, jess): This should be moved into plugins.
var SUPPORTED_PROVIDERS = [
    {
        icon: <icons_1.IconGithub size="xs"/>,
        providerIds: ['github', 'integrations:github', 'integrations:github_enterprise'],
        commitUrl: function (_a) {
            var baseUrl = _a.baseUrl, commitId = _a.commitId;
            return baseUrl + "/commit/" + commitId;
        },
    },
    {
        icon: <icons_1.IconBitbucket size="xs"/>,
        providerIds: ['bitbucket', 'integrations:bitbucket'],
        commitUrl: function (_a) {
            var baseUrl = _a.baseUrl, commitId = _a.commitId;
            return baseUrl + "/commits/" + commitId;
        },
    },
    {
        icon: <icons_1.IconVsts size="xs"/>,
        providerIds: ['visualstudio', 'integrations:vsts'],
        commitUrl: function (_a) {
            var baseUrl = _a.baseUrl, commitId = _a.commitId;
            return baseUrl + "/commit/" + commitId;
        },
    },
    {
        icon: <icons_1.IconGitlab size="xs"/>,
        providerIds: ['gitlab', 'integrations:gitlab'],
        commitUrl: function (_a) {
            var baseUrl = _a.baseUrl, commitId = _a.commitId;
            return baseUrl + "/commit/" + commitId;
        },
    },
];
function CommitLink(_a) {
    var inline = _a.inline, commitId = _a.commitId, repository = _a.repository;
    if (!commitId || !repository) {
        return <span>{locale_1.t('Unknown Commit')}</span>;
    }
    var shortId = utils_1.getShortCommitHash(commitId);
    var providerData = SUPPORTED_PROVIDERS.find(function (provider) {
        if (!repository.provider) {
            return false;
        }
        return provider.providerIds.includes(repository.provider.id);
    });
    if (providerData === undefined) {
        return <span>{shortId}</span>;
    }
    var commitUrl = repository.url &&
        providerData.commitUrl({
            commitId: commitId,
            baseUrl: repository.url,
        });
    return !inline ? (<button_1.default external href={commitUrl} size="small" icon={providerData.icon}>
      {shortId}
    </button_1.default>) : (<externalLink_1.default className="inline-commit" href={commitUrl}>
      {providerData.icon}
      {' ' + shortId}
    </externalLink_1.default>);
}
exports.default = CommitLink;
//# sourceMappingURL=commitLink.jsx.map