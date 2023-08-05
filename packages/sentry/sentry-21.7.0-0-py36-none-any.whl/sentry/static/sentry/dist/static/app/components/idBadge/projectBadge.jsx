Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var badgeDisplayName_1 = tslib_1.__importDefault(require("app/components/idBadge/badgeDisplayName"));
var baseBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/baseBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var ProjectBadge = function (_a) {
    var project = _a.project, organization = _a.organization, to = _a.to, _b = _a.hideOverflow, hideOverflow = _b === void 0 ? true : _b, _c = _a.disableLink, disableLink = _c === void 0 ? false : _c, props = tslib_1.__rest(_a, ["project", "organization", "to", "hideOverflow", "disableLink"]);
    var slug = project.slug, id = project.id;
    var badge = (<baseBadge_1.default displayName={<badgeDisplayName_1.default hideOverflow={hideOverflow}>{slug}</badgeDisplayName_1.default>} project={project} {...props}/>);
    if (!disableLink && (organization === null || organization === void 0 ? void 0 : organization.slug)) {
        var defaultTo = "/organizations/" + organization.slug + "/projects/" + slug + "/" + (id ? "?project=" + id : '');
        return <StyledLink to={to !== null && to !== void 0 ? to : defaultTo}>{badge}</StyledLink>;
    }
    return badge;
};
var StyledLink = styled_1.default(link_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 0;\n\n  img:hover {\n    cursor: pointer;\n  }\n"], ["\n  flex-shrink: 0;\n\n  img:hover {\n    cursor: pointer;\n  }\n"])));
exports.default = withOrganization_1.default(ProjectBadge);
var templateObject_1;
//# sourceMappingURL=projectBadge.jsx.map