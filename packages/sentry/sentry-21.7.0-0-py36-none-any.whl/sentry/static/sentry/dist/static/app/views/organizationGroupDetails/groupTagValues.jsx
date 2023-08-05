Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupTagValues = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var property_1 = tslib_1.__importDefault(require("lodash/property"));
var sortBy_1 = tslib_1.__importDefault(require("lodash/sortBy"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var dataExport_1 = tslib_1.__importStar(require("app/components/dataExport"));
var deviceName_1 = tslib_1.__importDefault(require("app/components/deviceName"));
var detailedError_1 = tslib_1.__importDefault(require("app/components/errors/detailedError"));
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var userBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/userBadge"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var GroupTagValues = /** @class */ (function (_super) {
    tslib_1.__extends(GroupTagValues, _super);
    function GroupTagValues() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GroupTagValues.prototype.getEndpoints = function () {
        var environment = this.props.environments;
        var _a = this.props.params, groupId = _a.groupId, tagKey = _a.tagKey;
        return [
            ['tag', "/issues/" + groupId + "/tags/" + tagKey + "/"],
            [
                'tagValueList',
                "/issues/" + groupId + "/tags/" + tagKey + "/values/",
                { query: { environment: environment } },
            ],
        ];
    };
    GroupTagValues.prototype.renderBody = function () {
        var _a = this.props, group = _a.group, _b = _a.params, orgId = _b.orgId, tagKey = _b.tagKey, environments = _a.environments;
        var _c = this.state, tag = _c.tag, tagValueList = _c.tagValueList, tagValueListPageLinks = _c.tagValueListPageLinks;
        var sortedTagValueList = sortBy_1.default(tagValueList, property_1.default('count')).reverse();
        if (sortedTagValueList.length === 0 && environments.length > 0) {
            return (<detailedError_1.default heading={locale_1.t('Sorry, the tags for this issue could not be found.')} message={locale_1.t('No tags were found for the currently selected environments')}/>);
        }
        var issuesPath = "/organizations/" + orgId + "/issues/";
        var children = sortedTagValueList.map(function (tagValue, tagValueIdx) {
            var _a;
            var pct = tag.totalValues
                ? utils_1.percent(tagValue.count, tag.totalValues).toFixed(2) + "%"
                : '--';
            var query = tagValue.query || tag.key + ":\"" + tagValue.value + "\"";
            return (<tr key={tagValueIdx}>
          <td className="bar-cell">
            <span className="label">{pct}</span>
          </td>
          <td>
            <ValueWrapper>
              <globalSelectionLink_1.default to={{
                    pathname: issuesPath,
                    query: { query: query },
                }}>
                {tag.key === 'user' ? (<userBadge_1.default user={tslib_1.__assign(tslib_1.__assign({}, tagValue), { id: (_a = tagValue.identifier) !== null && _a !== void 0 ? _a : '' })} avatarSize={20} hideEmail/>) : (<deviceName_1.default value={tagValue.name}/>)}
              </globalSelectionLink_1.default>
              {tagValue.email && (<StyledExternalLink href={"mailto:" + tagValue.email}>
                  <icons_1.IconMail size="xs" color="gray300"/>
                </StyledExternalLink>)}
              {utils_1.isUrl(tagValue.value) && (<StyledExternalLink href={tagValue.value}>
                  <icons_1.IconOpen size="xs" color="gray300"/>
                </StyledExternalLink>)}
            </ValueWrapper>
          </td>
          <td>
            <timeSince_1.default date={tagValue.lastSeen}/>
          </td>
        </tr>);
        });
        return (<react_1.Fragment>
        <Header>
          <HeaderTitle>{tag.key === 'user' ? locale_1.t('Affected Users') : tag.name}</HeaderTitle>
          <HeaderButtons gap={1}>
            <BrowserExportButton size="small" priority="default" href={"/" + orgId + "/" + group.project.slug + "/issues/" + group.id + "/tags/" + tagKey + "/export/"}>
              {locale_1.t('Export Page to CSV')}
            </BrowserExportButton>
            <dataExport_1.default payload={{
                queryType: dataExport_1.ExportQueryType.IssuesByTag,
                queryInfo: {
                    project: group.project.id,
                    group: group.id,
                    key: tagKey,
                },
            }}/>
          </HeaderButtons>
        </Header>
        <StyledTable className="table">
          <thead>
            <tr>
              <TableHeader width={20}>%</TableHeader>
              <th />
              <TableHeader width={300}>{locale_1.t('Last Seen')}</TableHeader>
            </tr>
          </thead>
          <tbody>{children}</tbody>
        </StyledTable>
        <pagination_1.default pageLinks={tagValueListPageLinks}/>
        <p>
          <small>
            {locale_1.t('Note: Percentage of issue is based on events seen in the last 7 days.')}
          </small>
        </p>
      </react_1.Fragment>);
    };
    return GroupTagValues;
}(asyncComponent_1.default));
exports.GroupTagValues = GroupTagValues;
var StyledTable = styled_1.default('table')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  > tbody > tr:nth-of-type(odd) {\n    background-color: ", ";\n  }\n"], ["\n  > tbody > tr:nth-of-type(odd) {\n    background-color: ", ";\n  }\n"])), function (p) { return p.theme.bodyBackground; });
var Header = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0 0 20px;\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0 0 20px;\n"])));
var HeaderTitle = styled_1.default('h3')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var HeaderButtons = styled_1.default(buttonBar_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  align-items: stretch;\n  margin: 0px ", ";\n"], ["\n  align-items: stretch;\n  margin: 0px ", ";\n"])), space_1.default(1.5));
var BrowserExportButton = styled_1.default(button_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var TableHeader = styled_1.default('th')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  width: ", "px;\n"], ["\n  width: ", "px;\n"])), function (p) { return p.width; });
var ValueWrapper = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledExternalLink = styled_1.default(externalLink_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(0.5));
exports.default = GroupTagValues;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=groupTagValues.jsx.map