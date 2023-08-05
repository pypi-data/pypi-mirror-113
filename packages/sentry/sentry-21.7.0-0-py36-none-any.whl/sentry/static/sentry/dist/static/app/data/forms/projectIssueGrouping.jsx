Object.defineProperty(exports, "__esModule", { value: true });
exports.fields = exports.route = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var groupingInfo_1 = require("app/components/events/groupingInfo");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var marked_1 = tslib_1.__importDefault(require("app/utils/marked"));
// Export route to make these forms searchable by label/help
exports.route = '/settings/:orgId/projects/:projectId/issue-grouping/';
var groupingConfigField = {
    name: 'groupingConfig',
    type: 'select',
    label: locale_1.t('Grouping Config'),
    saveOnBlur: false,
    saveMessageAlertType: 'info',
    saveMessage: locale_1.t('Changing grouping config will apply to future events only (can take up to a minute).'),
    selectionInfoFunction: function (args) {
        var groupingConfigs = args.groupingConfigs, value = args.value;
        var selection = groupingConfigs.find(function (_a) {
            var id = _a.id;
            return id === value;
        });
        var changelog = (selection === null || selection === void 0 ? void 0 : selection.changelog) || '';
        if (!changelog) {
            return null;
        }
        return (<Changelog>
        <ChangelogTitle>
          {locale_1.tct('New in version [version]', { version: selection.id })}:
        </ChangelogTitle>
        <div dangerouslySetInnerHTML={{ __html: marked_1.default(changelog) }}/>
      </Changelog>);
    },
    choices: function (_a) {
        var groupingConfigs = _a.groupingConfigs;
        return groupingConfigs.map(function (_a) {
            var id = _a.id, hidden = _a.hidden;
            return [
                id.toString(),
                <groupingInfo_1.GroupingConfigItem key={id} isHidden={hidden}>
        {id}
      </groupingInfo_1.GroupingConfigItem>,
            ];
        });
    },
    help: locale_1.t('Sets the grouping algorithm to be used for new events.'),
    visible: function (_a) {
        var features = _a.features;
        return features.has('set-grouping-config');
    },
};
exports.fields = {
    fingerprintingRules: {
        name: 'fingerprintingRules',
        type: 'string',
        label: locale_1.t('Fingerprint Rules'),
        hideLabel: true,
        placeholder: locale_1.t('error.type:MyException -> fingerprint-value\nstack.function:some_panic_function -> fingerprint-value'),
        multiline: true,
        monospace: true,
        autosize: true,
        inline: false,
        maxRows: 20,
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: locale_1.t('Changing fingerprint rules will apply to future events only (can take up to a minute).'),
        formatMessageValue: false,
        help: function () { return (<react_1.Fragment>
        <RuleDescription>
          {locale_1.tct("This can be used to modify the fingerprint rules on the server with custom rules.\n        Rules follow the pattern [pattern]. To learn more about fingerprint rules, [docs:read the docs].", {
                pattern: <code>matcher:glob -&gt; fingerprint, values</code>,
                docs: (<externalLink_1.default href="https://docs.sentry.io/product/data-management-settings/event-grouping/fingerprint-rules/"/>),
            })}
        </RuleDescription>
        <RuleExample>
          {"# force all errors of the same type to have the same fingerprint\nerror.type:DatabaseUnavailable -> system-down\n# force all memory allocation errors to be grouped together\nstack.function:malloc -> memory-allocation-error"}
        </RuleExample>
      </react_1.Fragment>); },
        visible: true,
    },
    groupingEnhancements: {
        name: 'groupingEnhancements',
        type: 'string',
        label: locale_1.t('Stack Trace Rules'),
        hideLabel: true,
        placeholder: locale_1.t('stack.function:raise_an_exception ^-group\nstack.function:namespace::* +app'),
        multiline: true,
        monospace: true,
        autosize: true,
        inline: false,
        maxRows: 20,
        saveOnBlur: false,
        saveMessageAlertType: 'info',
        saveMessage: locale_1.t('Changing stack trace rules will apply to future events only (can take up to a minute).'),
        formatMessageValue: false,
        help: function () { return (<react_1.Fragment>
        <RuleDescription>
          {locale_1.tct("This can be used to enhance the grouping algorithm with custom rules.\n        Rules follow the pattern [pattern]. To learn more about stack trace rules, [docs:read the docs].", {
                pattern: <code>matcher:glob [v^]?[+-]flag</code>,
                docs: (<externalLink_1.default href="https://docs.sentry.io/product/data-management-settings/event-grouping/stack-trace-rules/"/>),
            })}
        </RuleDescription>
        <RuleExample>
          {"# remove all frames above a certain function from grouping\nstack.function:panic_handler ^-group\n# mark all functions following a prefix in-app\nstack.function:mylibrary_* +app"}
        </RuleExample>
      </react_1.Fragment>); },
        validate: function () { return []; },
        visible: true,
    },
    groupingConfig: groupingConfigField,
    secondaryGroupingConfig: tslib_1.__assign(tslib_1.__assign({}, groupingConfigField), { name: 'secondaryGroupingConfig', label: locale_1.t('Fallback/Secondary Grouping Config'), help: locale_1.t('Sets the secondary grouping algorithm that should be run in addition to avoid creating too many new groups. Controlled by expiration date below.') }),
    secondaryGroupingExpiry: {
        name: 'secondaryGroupingExpiry',
        type: 'number',
        label: locale_1.t('Expiration date of secondary grouping'),
        help: locale_1.t('If this UNIX timestamp is in the past, the secondary grouping configuration stops applying automatically.'),
    },
};
var RuleDescription = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  margin-top: -", ";\n  margin-right: 36px;\n"], ["\n  margin-bottom: ", ";\n  margin-top: -", ";\n  margin-right: 36px;\n"])), space_1.default(1), space_1.default(1));
var RuleExample = styled_1.default('pre')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  margin-right: 36px;\n"], ["\n  margin-bottom: ", ";\n  margin-right: 36px;\n"])), space_1.default(1));
var Changelog = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  top: -1px;\n  margin-bottom: -1px;\n  padding: ", ";\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  font-size: ", ";\n\n  &:last-child {\n    border: 0;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n"], ["\n  position: relative;\n  top: -1px;\n  margin-bottom: -1px;\n  padding: ", ";\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  font-size: ", ";\n\n  &:last-child {\n    border: 0;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n"])), space_1.default(2), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var ChangelogTitle = styled_1.default('h3')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", " !important;\n"], ["\n  font-size: ", ";\n  margin-bottom: ", " !important;\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(0.75));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=projectIssueGrouping.jsx.map