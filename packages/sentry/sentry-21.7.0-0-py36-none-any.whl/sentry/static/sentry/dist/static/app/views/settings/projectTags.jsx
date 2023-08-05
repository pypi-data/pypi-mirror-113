Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/project/permissionAlert"));
var ProjectTags = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectTags, _super);
    function ProjectTags() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (key, idx) { return function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var params, projectId, orgId, tags, error_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        params = this.props.params;
                        projectId = params.projectId, orgId = params.orgId;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/tags/" + key + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _a.sent();
                        tags = tslib_1.__spreadArray([], tslib_1.__read(this.state.tags));
                        tags.splice(idx, 1);
                        this.setState({ tags: tags });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _a.sent();
                        this.setState({ error: true, loading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); }; };
        return _this;
    }
    ProjectTags.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { tags: [] });
    };
    ProjectTags.prototype.getEndpoints = function () {
        var _a = this.props.params, projectId = _a.projectId, orgId = _a.orgId;
        return [['tags', "/projects/" + orgId + "/" + projectId + "/tags/"]];
    };
    ProjectTags.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('Tags'), projectId, false);
    };
    ProjectTags.prototype.renderBody = function () {
        var _this = this;
        var tags = this.state.tags;
        var isEmpty = !tags || !tags.length;
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('Tags')}/>
        <permissionAlert_1.default />

        <textBlock_1.default>
          {locale_1.tct("Each event in Sentry may be annotated with various tags (key and value pairs).\n                 Learn how to [link:add custom tags].", {
                link: (<externalLink_1.default href="https://docs.sentry.io/platform-redirect/?next=/enriching-events/tags/"/>),
            })}
        </textBlock_1.default>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Tags')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            {isEmpty ? (<emptyMessage_1.default>
                {locale_1.tct('There are no tags, [link:learn how to add tags]', {
                    link: (<externalLink_1.default href="https://docs.sentry.io/product/sentry-basics/guides/enrich-data/"/>),
                })}
              </emptyMessage_1.default>) : (<access_1.default access={['project:write']}>
                {function (_a) {
                    var hasAccess = _a.hasAccess;
                    return tags.map(function (_a, idx) {
                        var key = _a.key, canDelete = _a.canDelete;
                        var enabled = canDelete && hasAccess;
                        return (<TagPanelItem key={key} data-test-id="tag-row">
                        <TagName>{key}</TagName>
                        <Actions>
                          <confirm_1.default message={locale_1.t('Are you sure you want to remove this tag?')} onConfirm={_this.handleDelete(key, idx)} disabled={!enabled}>
                            <button_1.default size="xsmall" title={enabled
                                ? locale_1.t('Remove tag')
                                : hasAccess
                                    ? locale_1.t('This tag cannot be deleted.')
                                    : locale_1.t('You do not have permission to remove tags.')} icon={<icons_1.IconDelete size="xs"/>} data-test-id="delete"/>
                          </confirm_1.default>
                        </Actions>
                      </TagPanelItem>);
                    });
                }}
              </access_1.default>)}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    };
    return ProjectTags;
}(asyncView_1.default));
exports.default = ProjectTags;
var TagPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n  align-items: center;\n"], ["\n  padding: 0;\n  align-items: center;\n"])));
var TagName = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  padding: ", ";\n"], ["\n  flex: 1;\n  padding: ", ";\n"])), space_1.default(2));
var Actions = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"])), space_1.default(2));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=projectTags.jsx.map