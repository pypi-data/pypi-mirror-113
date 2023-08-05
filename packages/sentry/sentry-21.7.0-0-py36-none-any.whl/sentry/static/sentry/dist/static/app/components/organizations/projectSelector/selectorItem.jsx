Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var globalSelectionHeaderRow_1 = tslib_1.__importDefault(require("app/components/globalSelectionHeaderRow"));
var highlight_1 = tslib_1.__importDefault(require("app/components/highlight"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var bookmarkStar_1 = tslib_1.__importDefault(require("app/components/projects/bookmarkStar"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var animations_1 = require("app/styles/animations");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var defaultProps = {
    multi: false,
    inputValue: '',
    isChecked: false,
};
var ProjectSelectorItem = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectSelectorItem, _super);
    function ProjectSelectorItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            bookmarkHasChanged: false,
        };
        _this.handleClick = function (event) {
            var _a = _this.props, project = _a.project, onMultiSelect = _a.onMultiSelect;
            event.stopPropagation();
            if (onMultiSelect) {
                onMultiSelect(project, event);
            }
        };
        _this.handleBookmarkToggle = function (isBookmarked) {
            var organization = _this.props.organization;
            analytics_1.analytics('projectselector.bookmark_toggle', {
                org_id: parseInt(organization.id, 10),
                bookmarked: isBookmarked,
            });
        };
        _this.clearAnimation = function () {
            _this.setState({ bookmarkHasChanged: false });
        };
        return _this;
    }
    ProjectSelectorItem.prototype.componentDidUpdate = function (nextProps) {
        if (nextProps.project.isBookmarked !== this.props.project.isBookmarked) {
            this.setBookmarkHasChanged();
        }
    };
    ProjectSelectorItem.prototype.setBookmarkHasChanged = function () {
        this.setState({ bookmarkHasChanged: true });
    };
    ProjectSelectorItem.prototype.renderDisabledCheckbox = function (_a) {
        var children = _a.children, features = _a.features;
        return (<hovercard_1.default body={<featureDisabled_1.default features={features} hideHelpToggle message={locale_1.t('Multiple project selection disabled')} featureName={locale_1.t('Multiple Project Selection')}/>}>
        {children}
      </hovercard_1.default>);
    };
    ProjectSelectorItem.prototype.render = function () {
        var _this = this;
        var _a = this.props, project = _a.project, multi = _a.multi, inputValue = _a.inputValue, isChecked = _a.isChecked, organization = _a.organization;
        var bookmarkHasChanged = this.state.bookmarkHasChanged;
        return (<BadgeAndActionsWrapper bookmarkHasChanged={bookmarkHasChanged} onAnimationEnd={this.clearAnimation}>
        <globalSelectionHeaderRow_1.default checked={isChecked} onCheckClick={this.handleClick} multi={multi} renderCheckbox={function (_a) {
                var checkbox = _a.checkbox;
                return (<feature_1.default features={['organizations:global-views']} hookName="feature-disabled:project-selector-checkbox" renderDisabled={_this.renderDisabledCheckbox}>
              {checkbox}
            </feature_1.default>);
            }}>
          <BadgeWrapper isMulti={multi}>
            <idBadge_1.default project={project} avatarSize={16} displayName={<highlight_1.default text={inputValue}>{project.slug}</highlight_1.default>} avatarProps={{ consistentWidth: true }} disableLink/>
          </BadgeWrapper>
          <StyledBookmarkStar project={project} organization={organization} bookmarkHasChanged={bookmarkHasChanged} onToggle={this.handleBookmarkToggle}/>
          <StyledLink to={"/organizations/" + organization.slug + "/projects/" + project.slug + "/?project=" + project.id} onClick={function (e) { return e.stopPropagation(); }}>
            <icons_1.IconOpen />
          </StyledLink>

          <StyledLink to={"/settings/" + organization.slug + "/" + project.slug + "/"} onClick={function (e) { return e.stopPropagation(); }}>
            <icons_1.IconSettings />
          </StyledLink>
        </globalSelectionHeaderRow_1.default>
      </BadgeAndActionsWrapper>);
    };
    ProjectSelectorItem.defaultProps = defaultProps;
    return ProjectSelectorItem;
}(React.PureComponent));
exports.default = ProjectSelectorItem;
var StyledBookmarkStar = styled_1.default(bookmarkStar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  box-sizing: content-box;\n  opacity: ", ";\n  transition: 0.5s opacity ease-out;\n  display: block;\n  width: 14px;\n  height: 14px;\n  margin-top: -", "; /* trivial alignment bump */\n  ", ";\n"], ["\n  padding: ", " ", ";\n  box-sizing: content-box;\n  opacity: ", ";\n  transition: 0.5s opacity ease-out;\n  display: block;\n  width: 14px;\n  height: 14px;\n  margin-top: -", "; /* trivial alignment bump */\n  ", ";\n"])), space_1.default(1), space_1.default(0.5), function (p) { return (p.project.isBookmarked ? 1 : 0.33); }, space_1.default(0.25), function (p) {
    return p.bookmarkHasChanged && react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n      animation: 0.5s ", ";\n    "], ["\n      animation: 0.5s ", ";\n    "])), animations_1.pulse(1.4));
});
var BadgeWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  ", ";\n  white-space: nowrap;\n  overflow: hidden;\n"], ["\n  display: flex;\n  flex: 1;\n  ", ";\n  white-space: nowrap;\n  overflow: hidden;\n"])), function (p) { return !p.isMulti && 'flex: 1'; });
var StyledLink = styled_1.default(link_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", " ", " ", " ", ";\n  opacity: 0.33;\n  transition: 0.5s opacity ease-out;\n  :hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", " ", " ", " ", ";\n  opacity: 0.33;\n  transition: 0.5s opacity ease-out;\n  :hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, space_1.default(1), space_1.default(0.25), space_1.default(1), space_1.default(1), function (p) { return p.theme.textColor; });
var BadgeAndActionsWrapper = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  ", ";\n  z-index: ", ";\n  position: relative;\n  border-style: solid;\n  border-width: 1px 0;\n  border-color: transparent;\n  :hover {\n    ", " {\n      opacity: 1;\n    }\n    ", " {\n      opacity: 1;\n    }\n  }\n"], ["\n  ", ";\n  z-index: ", ";\n  position: relative;\n  border-style: solid;\n  border-width: 1px 0;\n  border-color: transparent;\n  :hover {\n    ", " {\n      opacity: 1;\n    }\n    ", " {\n      opacity: 1;\n    }\n  }\n"])), function (p) {
    return p.bookmarkHasChanged && react_1.css(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n      animation: 1s ", ";\n    "], ["\n      animation: 1s ", ";\n    "])), animations_1.alertHighlight('info', p.theme));
}, function (p) { return (p.bookmarkHasChanged ? 1 : 'inherit'); }, StyledBookmarkStar, StyledLink);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=selectorItem.jsx.map