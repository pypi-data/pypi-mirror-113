Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var icons_1 = require("app/icons");
var pluginIcon_1 = tslib_1.__importDefault(require("app/plugins/components/pluginIcon"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var highlightFuseMatches_1 = tslib_1.__importDefault(require("app/utils/highlightFuseMatches"));
var settingsSearch_1 = require("app/views/settings/components/settingsSearch");
var SearchResult = /** @class */ (function (_super) {
    tslib_1.__extends(SearchResult, _super);
    function SearchResult() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SearchResult.prototype.renderContent = function () {
        var _a;
        var _b = this.props, highlighted = _b.highlighted, item = _b.item, matches = _b.matches, params = _b.params;
        var sourceType = item.sourceType, model = item.model, extra = item.extra;
        var title = item.title, description = item.description;
        if (matches) {
            // TODO(ts) Type this better.
            var HighlightedMarker = function (p) { return (<HighlightMarker highlighted={highlighted} {...p}/>); };
            var matchedTitle = matches && matches.find(function (_a) {
                var key = _a.key;
                return key === 'title';
            });
            var matchedDescription = matches && matches.find(function (_a) {
                var key = _a.key;
                return key === 'description';
            });
            title = matchedTitle
                ? highlightFuseMatches_1.default(matchedTitle, HighlightedMarker)
                : title;
            description = matchedDescription
                ? highlightFuseMatches_1.default(matchedDescription, HighlightedMarker)
                : description;
        }
        if (['organization', 'member', 'project', 'team'].includes(sourceType)) {
            var DescriptionNode = (<BadgeDetail highlighted={highlighted}>{description}</BadgeDetail>);
            var badgeProps = (_a = {
                    displayName: title,
                    displayEmail: DescriptionNode,
                    description: DescriptionNode,
                    useLink: false,
                    orgId: params.orgId,
                    avatarSize: 32
                },
                _a[sourceType] = model,
                _a);
            return <idBadge_1.default {...badgeProps}/>;
        }
        return (<react_1.Fragment>
        <div>
          <SearchTitle>{title}</SearchTitle>
        </div>
        {description && <SearchDetail>{description}</SearchDetail>}
        {extra && <ExtraDetail>{extra}</ExtraDetail>}
      </react_1.Fragment>);
    };
    SearchResult.prototype.renderResultType = function () {
        var item = this.props.item;
        var resultType = item.resultType, model = item.model;
        var isSettings = resultType === 'settings';
        var isField = resultType === 'field';
        var isRoute = resultType === 'route';
        var isIntegration = resultType === 'integration';
        if (isSettings) {
            return <icons_1.IconSettings />;
        }
        if (isField) {
            return <icons_1.IconInput />;
        }
        if (isRoute) {
            return <icons_1.IconLink />;
        }
        if (isIntegration) {
            return <StyledPluginIcon pluginId={model.slug}/>;
        }
        return null;
    };
    SearchResult.prototype.render = function () {
        return (<Wrapper>
        <Content>{this.renderContent()}</Content>
        <IconWrapper>{this.renderResultType()}</IconWrapper>
      </Wrapper>);
    };
    return SearchResult;
}(react_1.Component));
exports.default = react_router_1.withRouter(SearchResult);
// This is for tests
var SearchTitle = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject([""], [""])));
var SearchDetail = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: 0.8em;\n  line-height: 1.3;\n  margin-top: 4px;\n  opacity: 0.8;\n"], ["\n  font-size: 0.8em;\n  line-height: 1.3;\n  margin-top: 4px;\n  opacity: 0.8;\n"])));
var ExtraDetail = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  margin-top: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  margin-top: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, space_1.default(0.5));
var BadgeDetail = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  line-height: 1.3;\n  color: ", ";\n"], ["\n  line-height: 1.3;\n  color: ", ";\n"])), function (p) { return (p.highlighted ? p.theme.purple300 : null); });
var Wrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
var Content = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var IconWrapper = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  ", " & {\n    color: inherit;\n  }\n"], ["\n  " /* sc-selector */, " & {\n    color: inherit;\n  }\n"])), /* sc-selector */ settingsSearch_1.StyledSettingsSearch);
var StyledPluginIcon = styled_1.default(pluginIcon_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var HighlightMarker = styled_1.default('mark')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n  background: transparent;\n  font-weight: bold;\n  color: ", ";\n"], ["\n  padding: 0;\n  background: transparent;\n  font-weight: bold;\n  color: ", ";\n"])), function (p) { return p.theme.active; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=searchResult.jsx.map