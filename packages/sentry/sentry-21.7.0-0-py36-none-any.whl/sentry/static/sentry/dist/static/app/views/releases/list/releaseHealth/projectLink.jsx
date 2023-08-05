Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
var locale_1 = require("app/locale");
var ProjectLink = function (_a) {
    var orgSlug = _a.orgSlug, releaseVersion = _a.releaseVersion, project = _a.project, location = _a.location;
    return (<button_1.default size="xsmall" to={{
            pathname: "/organizations/" + orgSlug + "/releases/" + encodeURIComponent(releaseVersion) + "/",
            query: tslib_1.__assign(tslib_1.__assign({}, utils_1.extractSelectionParameters(location.query)), { project: project.id, yAxis: undefined }),
        }}>
    {locale_1.t('View')}
  </button_1.default>);
};
exports.default = ProjectLink;
//# sourceMappingURL=projectLink.jsx.map