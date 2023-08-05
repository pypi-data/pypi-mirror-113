Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var editableText_1 = tslib_1.__importDefault(require("app/components/editableText"));
var thirds_1 = require("app/components/layouts/thirds");
var locale_1 = require("app/locale");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var utils_1 = require("./savedQuery/utils");
var NAME_DEFAULT = locale_1.t('Untitled query');
/**
 * Allows user to edit the name of the query.
 * By pressing Enter or clicking outside the component, the changes will be saved, if valid.
 */
function EventInputName(_a) {
    var api = _a.api, organization = _a.organization, eventView = _a.eventView, savedQuery = _a.savedQuery;
    function handleChange(nextQueryName) {
        // Do not update automatically if
        // 1) It is a new query
        // 2) The new name is same as the old name
        if (!savedQuery || savedQuery.name === nextQueryName) {
            return;
        }
        // This ensures that we are updating SavedQuery.name only.
        // Changes on QueryBuilder table will not be saved.
        var nextEventView = eventView_1.default.fromSavedQuery(tslib_1.__assign(tslib_1.__assign({}, savedQuery), { name: nextQueryName }));
        utils_1.handleUpdateQueryName(api, organization, nextEventView).then(function (_updatedQuery) {
            // The current eventview may have changes that are not explicitly saved.
            // So, we just preserve them and change its name
            var renamedEventView = eventView.clone();
            renamedEventView.name = nextQueryName;
            react_router_1.browserHistory.push(renamedEventView.getResultsViewUrlTarget(organization.slug));
        });
    }
    var value = eventView.name || NAME_DEFAULT;
    return (<StyledTitle data-test-id={"discover2-query-name-" + value}>
      <editableText_1.default value={value} onChange={handleChange} isDisabled={!eventView.id} errorMessage={locale_1.t('Please set a name for this query')}/>
    </StyledTitle>);
}
var StyledTitle = styled_1.default(thirds_1.Title)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  overflow: unset;\n"], ["\n  overflow: unset;\n"])));
exports.default = withApi_1.default(EventInputName);
var templateObject_1;
//# sourceMappingURL=eventInputName.jsx.map