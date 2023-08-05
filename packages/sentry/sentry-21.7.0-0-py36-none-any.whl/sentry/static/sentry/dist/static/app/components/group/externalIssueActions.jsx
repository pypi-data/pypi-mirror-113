Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var issueSyncListElement_1 = tslib_1.__importDefault(require("app/components/issueSyncListElement"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var integrationItem_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/integrationItem"));
var externalIssueForm_1 = tslib_1.__importDefault(require("./externalIssueForm"));
var ExternalIssueActions = function (_a) {
    var configurations = _a.configurations, group = _a.group, onChange = _a.onChange, api = _a.api;
    var _b = configurations
        .sort(function (a, b) { return a.name.toLowerCase().localeCompare(b.name.toLowerCase()); })
        .reduce(function (acc, curr) {
        if (curr.externalIssues.length) {
            acc.linked.push(curr);
        }
        else {
            acc.unlinked.push(curr);
        }
        return acc;
    }, { linked: [], unlinked: [] }), linked = _b.linked, unlinked = _b.unlinked;
    var deleteIssue = function (integration) {
        var externalIssues = integration.externalIssues;
        // Currently we do not support a case where there is multiple external issues.
        // For example, we shouldn't have more than 1 jira ticket created for an issue for each jira configuration.
        var issue = externalIssues[0];
        var id = issue.id;
        var endpoint = "/groups/" + group.id + "/integrations/" + integration.id + "/?externalIssue=" + id;
        api.request(endpoint, {
            method: 'DELETE',
            success: function () {
                onChange(function () { return indicator_1.addSuccessMessage(locale_1.t('Successfully unlinked issue.')); }, function () { return indicator_1.addErrorMessage(locale_1.t('Unable to unlink issue.')); });
            },
            error: function () {
                indicator_1.addErrorMessage(locale_1.t('Unable to unlink issue.'));
            },
        });
    };
    var doOpenModal = function (integration) {
        return modal_1.openModal(function (deps) { return (<externalIssueForm_1.default {...deps} {...{ group: group, onChange: onChange, integration: integration }}/>); });
    };
    return (<react_1.Fragment>
      {linked.map(function (config) {
            var provider = config.provider, externalIssues = config.externalIssues;
            var issue = externalIssues[0];
            return (<issueSyncListElement_1.default key={issue.id} externalIssueLink={issue.url} externalIssueId={issue.id} externalIssueKey={issue.key} externalIssueDisplayName={issue.displayName} onClose={function () { return deleteIssue(config); }} integrationType={provider.key} hoverCardHeader={locale_1.t('Linked %s Integration', provider.name)} hoverCardBody={<div>
                <IssueTitle>{issue.title}</IssueTitle>
                {issue.description && (<IssueDescription>{issue.description}</IssueDescription>)}
              </div>}/>);
        })}

      {unlinked.length > 0 && (<issueSyncListElement_1.default integrationType={unlinked[0].provider.key} hoverCardHeader={locale_1.t('Linked %s Integration', unlinked[0].provider.name)} hoverCardBody={<Container>
              {unlinked.map(function (config) { return (<Wrapper onClick={function () { return doOpenModal(config); }} key={config.id}>
                  <integrationItem_1.default integration={config}/>
                </Wrapper>); })}
            </Container>} onOpen={unlinked.length === 1 ? function () { return doOpenModal(unlinked[0]); } : undefined}/>)}
    </react_1.Fragment>);
};
var IssueTitle = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: 1.1em;\n  font-weight: 600;\n  ", ";\n"], ["\n  font-size: 1.1em;\n  font-weight: 600;\n  ", ";\n"])), overflowEllipsis_1.default);
var IssueDescription = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  ", ";\n"], ["\n  margin-top: ", ";\n  ", ";\n"])), space_1.default(1), overflowEllipsis_1.default);
var Wrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  cursor: pointer;\n"], ["\n  margin-bottom: ", ";\n  cursor: pointer;\n"])), space_1.default(2));
var Container = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  & > div:last-child {\n    margin-bottom: ", ";\n  }\n"], ["\n  & > div:last-child {\n    margin-bottom: ", ";\n  }\n"])), space_1.default(1));
exports.default = withApi_1.default(ExternalIssueActions);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=externalIssueActions.jsx.map