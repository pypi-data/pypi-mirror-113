Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var deviceName_1 = tslib_1.__importDefault(require("app/components/deviceName"));
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var GroupTags = /** @class */ (function (_super) {
    tslib_1.__extends(GroupTags, _super);
    function GroupTags() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            tagList: null,
            loading: true,
            error: false,
        };
        _this.fetchData = function () {
            var _a = _this.props, api = _a.api, group = _a.group, environments = _a.environments;
            _this.setState({
                loading: true,
                error: false,
            });
            api.request("/issues/" + group.id + "/tags/", {
                query: { environment: environments },
                success: function (data) {
                    _this.setState({
                        tagList: data,
                        error: false,
                        loading: false,
                    });
                },
                error: function () {
                    _this.setState({
                        error: true,
                        loading: false,
                    });
                },
            });
        };
        return _this;
    }
    GroupTags.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupTags.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual_1.default(prevProps.environments, this.props.environments)) {
            this.fetchData();
        }
    };
    GroupTags.prototype.getTagsDocsUrl = function () {
        return 'https://docs.sentry.io/platform-redirect/?next=/enriching-events/tags';
    };
    GroupTags.prototype.render = function () {
        var baseUrl = this.props.baseUrl;
        var children = [];
        if (this.state.loading) {
            return <loadingIndicator_1.default />;
        }
        else if (this.state.error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        if (this.state.tagList) {
            children = this.state.tagList.map(function (tag, tagIdx) {
                var valueChildren = tag.topValues.map(function (tagValue, tagValueIdx) {
                    var label = null;
                    var pct = utils_1.percent(tagValue.count, tag.totalValues);
                    var query = tagValue.query || tag.key + ":\"" + tagValue.value + "\"";
                    switch (tag.key) {
                        case 'release':
                            label = <version_1.default version={tagValue.name} anchor={false}/>;
                            break;
                        default:
                            label = <deviceName_1.default value={tagValue.name}/>;
                    }
                    return (<li key={tagValueIdx} data-test-id={tag.key}>
              <TagBarGlobalSelectionLink to={{
                            pathname: baseUrl + "events/",
                            query: { query: query },
                        }}>
                <TagBarBackground style={{ width: pct + '%' }}/>
                <TagBarLabel>{label}</TagBarLabel>
                <TagBarCount>
                  <count_1.default value={tagValue.count}/>
                </TagBarCount>
              </TagBarGlobalSelectionLink>
            </li>);
                });
                return (<TagItem key={tagIdx}>
            <panels_1.Panel>
              <panels_1.PanelHeader hasButtons style={{ textTransform: 'none' }}>
                <div style={{ fontSize: 16 }}>{tag.key}</div>
                <DetailsLinkWrapper>
                  <globalSelectionLink_1.default className="btn btn-default btn-sm" to={baseUrl + "tags/" + tag.key + "/"}>
                    {locale_1.t('More Details')}
                  </globalSelectionLink_1.default>
                </DetailsLinkWrapper>
              </panels_1.PanelHeader>
              <panels_1.PanelBody withPadding>
                <ul style={{ listStyleType: 'none', padding: 0, margin: 0 }}>
                  {valueChildren}
                </ul>
              </panels_1.PanelBody>
            </panels_1.Panel>
          </TagItem>);
            });
        }
        return (<div>
        <Container>{children}</Container>
        <alert_1.default type="info">
          {locale_1.tct('Tags are automatically indexed for searching and breakdown charts. Learn how to [link: add custom tags to issues]', {
                link: <a href={this.getTagsDocsUrl()}/>,
            })}
        </alert_1.default>
      </div>);
    };
    return GroupTags;
}(React.Component));
var DetailsLinkWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var Container = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n"])));
var TagItem = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: 0 ", ";\n  width: 50%;\n"], ["\n  padding: 0 ", ";\n  width: 50%;\n"])), space_1.default(1));
var TagBarBackground = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  left: 0;\n  background: ", ";\n  border-radius: ", ";\n"], ["\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  left: 0;\n  background: ", ";\n  border-radius: ", ";\n"])), function (p) { return p.theme.tagBar; }, function (p) { return p.theme.borderRadius; });
var TagBarGlobalSelectionLink = styled_1.default(globalSelectionLink_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: flex;\n  line-height: 2.2;\n  color: ", ";\n  margin-bottom: ", ";\n  padding: 0 ", ";\n  background: ", ";\n  border-radius: ", ";\n  overflow: hidden;\n\n  &:hover {\n    color: ", ";\n    text-decoration: underline;\n    ", " {\n      background: ", ";\n    }\n  }\n"], ["\n  position: relative;\n  display: flex;\n  line-height: 2.2;\n  color: ", ";\n  margin-bottom: ", ";\n  padding: 0 ", ";\n  background: ", ";\n  border-radius: ", ";\n  overflow: hidden;\n\n  &:hover {\n    color: ", ";\n    text-decoration: underline;\n    ", " {\n      background: ", ";\n    }\n  }\n"])), function (p) { return p.theme.textColor; }, space_1.default(0.5), space_1.default(1), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.textColor; }, TagBarBackground, function (p) { return p.theme.tagBarHover; });
var TagBarLabel = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  flex-grow: 1;\n  ", "\n"], ["\n  position: relative;\n  flex-grow: 1;\n  ", "\n"])), overflowEllipsis_1.default);
var TagBarCount = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  padding-left: ", ";\n"], ["\n  position: relative;\n  padding-left: ", ";\n"])), space_1.default(2));
exports.default = withApi_1.default(GroupTags);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=groupTags.jsx.map