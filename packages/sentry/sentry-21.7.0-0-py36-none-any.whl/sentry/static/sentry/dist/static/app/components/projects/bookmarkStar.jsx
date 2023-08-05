Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var projects_1 = require("app/actionCreators/projects");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var BookmarkStar = function (_a) {
    var api = _a.api, isBookmarkedProp = _a.isBookmarked, className = _a.className, organization = _a.organization, project = _a.project, onToggle = _a.onToggle;
    var isBookmarked = utils_1.defined(isBookmarkedProp)
        ? isBookmarkedProp
        : project.isBookmarked;
    var toggleProjectBookmark = function (event) {
        projects_1.update(api, {
            orgId: organization.slug,
            projectId: project.slug,
            data: { isBookmarked: !isBookmarked },
        }).catch(function () {
            indicator_1.addErrorMessage(locale_1.t('Unable to toggle bookmark for %s', project.slug));
        });
        // needed to dismiss tooltip
        document.activeElement.blur();
        // prevent dropdowns from closing
        event.stopPropagation();
        if (onToggle) {
            onToggle(!isBookmarked);
        }
    };
    return (<Star isBookmarked={isBookmarked} isSolid={isBookmarked} onClick={toggleProjectBookmark} className={className}/>);
};
var Star = styled_1.default(icons_1.IconStar, { shouldForwardProp: function (p) { return p !== 'isBookmarked'; } })(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  cursor: pointer;\n"], ["\n  color: ", ";\n  cursor: pointer;\n"])), function (p) { return (p.isBookmarked ? p.theme.yellow300 : p.theme.gray200); });
exports.default = withApi_1.default(BookmarkStar);
var templateObject_1;
//# sourceMappingURL=bookmarkStar.jsx.map