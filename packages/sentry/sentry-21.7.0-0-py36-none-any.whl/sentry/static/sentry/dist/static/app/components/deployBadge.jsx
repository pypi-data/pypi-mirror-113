Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var DeployBadge = function (_a) {
    var deploy = _a.deploy, orgSlug = _a.orgSlug, projectId = _a.projectId, version = _a.version, className = _a.className;
    var shouldLinkToIssues = !!orgSlug && !!version;
    var badge = (<tag_1.default className={className} type="highlight" icon={shouldLinkToIssues && <icons_1.IconOpen />} textMaxWidth={80} tooltipText={shouldLinkToIssues ? locale_1.t('Open In Issues') : undefined}>
      {deploy.environment}
    </tag_1.default>);
    if (!shouldLinkToIssues) {
        return badge;
    }
    return (<link_1.default to={{
            pathname: "/organizations/" + orgSlug + "/issues/",
            query: {
                project: projectId !== null && projectId !== void 0 ? projectId : null,
                environment: deploy.environment,
                query: new tokenizeSearch_1.QueryResults(["release:" + version]).formatString(),
            },
        }}>
      {badge}
    </link_1.default>);
};
exports.default = DeployBadge;
//# sourceMappingURL=deployBadge.jsx.map