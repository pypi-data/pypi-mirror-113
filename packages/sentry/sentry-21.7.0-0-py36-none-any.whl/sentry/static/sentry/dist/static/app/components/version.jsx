Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var clipboard_1 = tslib_1.__importDefault(require("app/components/clipboard"));
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var formatters_1 = require("app/utils/formatters");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var Version = function (_a) {
    var version = _a.version, organization = _a.organization, _b = _a.anchor, anchor = _b === void 0 ? true : _b, preserveGlobalSelection = _a.preserveGlobalSelection, tooltipRawVersion = _a.tooltipRawVersion, withPackage = _a.withPackage, projectId = _a.projectId, truncate = _a.truncate, className = _a.className, location = _a.location;
    var versionToDisplay = formatters_1.formatVersion(version, withPackage);
    var releaseDetailProjectId;
    if (projectId) {
        // we can override preserveGlobalSelection's project id
        releaseDetailProjectId = projectId;
    }
    else if (!(organization === null || organization === void 0 ? void 0 : organization.features.includes('global-views'))) {
        // we need this for users without global-views, otherwise they might get `This release may not be in your selected project`
        releaseDetailProjectId = location === null || location === void 0 ? void 0 : location.query.project;
    }
    var renderVersion = function () {
        if (anchor && (organization === null || organization === void 0 ? void 0 : organization.slug)) {
            var props = {
                to: {
                    pathname: "/organizations/" + (organization === null || organization === void 0 ? void 0 : organization.slug) + "/releases/" + encodeURIComponent(version) + "/",
                    query: releaseDetailProjectId ? { project: releaseDetailProjectId } : undefined,
                },
                className: className,
            };
            if (preserveGlobalSelection) {
                return (<globalSelectionLink_1.default {...props}>
            <VersionText truncate={truncate}>{versionToDisplay}</VersionText>
          </globalSelectionLink_1.default>);
            }
            else {
                return (<link_1.default {...props}>
            <VersionText truncate={truncate}>{versionToDisplay}</VersionText>
          </link_1.default>);
            }
        }
        return (<VersionText className={className} truncate={truncate}>
        {versionToDisplay}
      </VersionText>);
    };
    var renderTooltipContent = function () { return (<TooltipContent onClick={function (e) {
            e.stopPropagation();
        }}>
      <TooltipVersionWrapper>{version}</TooltipVersionWrapper>

      <clipboard_1.default value={version}>
        <TooltipClipboardIconWrapper>
          <icons_1.IconCopy size="xs" color="white"/>
        </TooltipClipboardIconWrapper>
      </clipboard_1.default>
    </TooltipContent>); };
    var getPopperStyles = function () {
        // if the version name is not a hash (sha1 or sha265) and we are not on mobile, allow tooltip to be as wide as 500px
        if (/(^[a-f0-9]{40}$)|(^[a-f0-9]{64}$)/.test(version)) {
            return undefined;
        }
        return react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n      @media (min-width: ", ") {\n        max-width: 500px;\n      }\n    "], ["\n      @media (min-width: ", ") {\n        max-width: 500px;\n      }\n    "])), theme_1.default.breakpoints[0]);
    };
    return (<tooltip_1.default title={renderTooltipContent()} disabled={!tooltipRawVersion} isHoverable containerDisplayMode={truncate ? 'block' : 'inline-block'} popperStyle={getPopperStyles()}>
      {renderVersion()}
    </tooltip_1.default>);
};
// TODO(matej): try to wrap version with this when truncate prop is true (in separate PR)
// const VersionWrapper = styled('div')`
//   ${overflowEllipsis};
//   max-width: 100%;
//   width: auto;
//   display: inline-block;
// `;
var VersionText = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.truncate &&
        "max-width: 100%;\n    display: block;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;";
});
var TooltipContent = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var TooltipVersionWrapper = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis_1.default);
var TooltipClipboardIconWrapper = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  position: relative;\n  bottom: -", ";\n\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  margin-left: ", ";\n  position: relative;\n  bottom: -", ";\n\n  &:hover {\n    cursor: pointer;\n  }\n"])), space_1.default(0.5), space_1.default(0.25));
exports.default = withOrganization_1.default(react_router_1.withRouter(Version));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=version.jsx.map