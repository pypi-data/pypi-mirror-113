Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var pills_1 = tslib_1.__importDefault(require("app/components/pills"));
var utils_1 = require("app/utils");
var eventTagsPill_1 = tslib_1.__importDefault(require("./eventTagsPill"));
var EventTags = function (_a) {
    var _b = _a.event.tags, tags = _b === void 0 ? [] : _b, organization = _a.organization, projectId = _a.projectId, location = _a.location, hasQueryFeature = _a.hasQueryFeature;
    if (!tags.length) {
        return null;
    }
    var orgSlug = organization.slug;
    var streamPath = "/organizations/" + orgSlug + "/issues/";
    var releasesPath = "/organizations/" + orgSlug + "/releases/";
    return (<pills_1.default>
      {tags.map(function (tag, index) { return (<eventTagsPill_1.default key={!utils_1.defined(tag.key) ? "tag-pill-" + index : tag.key} tag={tag} projectId={projectId} organization={organization} query={utils_1.generateQueryWithTag(location.query, tag)} streamPath={streamPath} releasesPath={releasesPath} hasQueryFeature={hasQueryFeature}/>); })}
    </pills_1.default>);
};
exports.default = EventTags;
//# sourceMappingURL=eventTags.jsx.map