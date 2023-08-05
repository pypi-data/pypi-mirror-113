Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var icons_1 = require("app/icons");
function renderIcon(repo) {
    if (!repo.provider) {
        return null;
    }
    var id = repo.provider.id;
    var providerId = id.includes(':') ? id.split(':').pop() : id;
    switch (providerId) {
        case 'github':
            return <icons_1.IconGithub size="xs"/>;
        case 'gitlab':
            return <icons_1.IconGitlab size="xs"/>;
        case 'bitbucket':
            return <icons_1.IconBitbucket size="xs"/>;
        default:
            return null;
    }
}
var PullRequestLink = function (_a) {
    var pullRequest = _a.pullRequest, repository = _a.repository, inline = _a.inline;
    var displayId = repository.name + " #" + pullRequest.id + ": " + pullRequest.title;
    return pullRequest.externalUrl ? (<externalLink_1.default className={inline ? 'inline-commit' : 'btn btn-default btn-sm'} href={pullRequest.externalUrl}>
      {renderIcon(repository)}
      {inline ? '' : ' '}
      {displayId}
    </externalLink_1.default>) : (<span>{displayId}</span>);
};
exports.default = PullRequestLink;
//# sourceMappingURL=pullRequestLink.jsx.map