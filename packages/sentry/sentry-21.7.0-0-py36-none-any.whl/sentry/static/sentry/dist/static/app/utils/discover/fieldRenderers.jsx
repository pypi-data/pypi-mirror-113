Object.defineProperty(exports, "__esModule", { value: true });
exports.getFieldFormatter = exports.getFieldRenderer = exports.getSortField = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var partial_1 = tslib_1.__importDefault(require("lodash/partial"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var duration_1 = tslib_1.__importDefault(require("app/components/duration"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var userBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/userBadge"));
var rowBar_1 = require("app/components/performance/waterfall/rowBar");
var utils_1 = require("app/components/performance/waterfall/utils");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var userMisery_1 = tslib_1.__importDefault(require("app/components/userMisery"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var locale_1 = require("app/locale");
var utils_2 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var fields_1 = require("app/utils/discover/fields");
var events_1 = require("app/utils/events");
var formatters_1 = require("app/utils/formatters");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var filter_1 = require("app/views/performance/transactionSummary/filter");
var arrayValue_1 = tslib_1.__importDefault(require("./arrayValue"));
var keyTransactionField_1 = tslib_1.__importDefault(require("./keyTransactionField"));
var styles_1 = require("./styles");
var teamKeyTransactionField_1 = tslib_1.__importDefault(require("./teamKeyTransactionField"));
var EmptyValueContainer = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var emptyValue = <EmptyValueContainer>{locale_1.t('n/a')}</EmptyValueContainer>;
/**
 * A mapping of field types to their rendering function.
 * This mapping is used when a field is not defined in SPECIAL_FIELDS
 * and the field is not being coerced to a link.
 *
 * This mapping should match the output sentry.utils.snuba:get_json_type
 */
var FIELD_FORMATTERS = {
    boolean: {
        isSortable: true,
        renderFunc: function (field, data) {
            var value = data[field] ? locale_1.t('true') : locale_1.t('false');
            return <styles_1.Container>{value}</styles_1.Container>;
        },
    },
    date: {
        isSortable: true,
        renderFunc: function (field, data) { return (<styles_1.Container>
        {data[field]
                ? getDynamicText_1.default({
                    value: <styles_1.StyledDateTime date={data[field]}/>,
                    fixed: 'timestamp',
                })
                : emptyValue}
      </styles_1.Container>); },
    },
    duration: {
        isSortable: true,
        renderFunc: function (field, data) { return (<styles_1.NumberContainer>
        {typeof data[field] === 'number' ? (<duration_1.default seconds={data[field] / 1000} fixedDigits={2} abbreviation/>) : (emptyValue)}
      </styles_1.NumberContainer>); },
    },
    integer: {
        isSortable: true,
        renderFunc: function (field, data) { return (<styles_1.NumberContainer>
        {typeof data[field] === 'number' ? <count_1.default value={data[field]}/> : emptyValue}
      </styles_1.NumberContainer>); },
    },
    number: {
        isSortable: true,
        renderFunc: function (field, data) { return (<styles_1.NumberContainer>
        {typeof data[field] === 'number' ? formatters_1.formatFloat(data[field], 4) : emptyValue}
      </styles_1.NumberContainer>); },
    },
    percentage: {
        isSortable: true,
        renderFunc: function (field, data) { return (<styles_1.NumberContainer>
        {typeof data[field] === 'number' ? formatters_1.formatPercentage(data[field]) : emptyValue}
      </styles_1.NumberContainer>); },
    },
    string: {
        isSortable: true,
        renderFunc: function (field, data) {
            // Some fields have long arrays in them, only show the tail of the data.
            var value = Array.isArray(data[field])
                ? data[field].slice(-1)
                : utils_2.defined(data[field])
                    ? data[field]
                    : emptyValue;
            return <styles_1.Container>{value}</styles_1.Container>;
        },
    },
    array: {
        isSortable: true,
        renderFunc: function (field, data) {
            var value = Array.isArray(data[field]) ? data[field] : [data[field]];
            return <arrayValue_1.default value={value}/>;
        },
    },
};
/**
 * "Special fields" either do not map 1:1 to an single column in the event database,
 * or they require custom UI formatting that can't be handled by the datatype formatters.
 */
var SPECIAL_FIELDS = {
    id: {
        sortField: 'id',
        renderFunc: function (data) {
            var id = data === null || data === void 0 ? void 0 : data.id;
            if (typeof id !== 'string') {
                return null;
            }
            return <styles_1.Container>{events_1.getShortEventId(id)}</styles_1.Container>;
        },
    },
    trace: {
        sortField: 'trace',
        renderFunc: function (data) {
            var id = data === null || data === void 0 ? void 0 : data.trace;
            if (typeof id !== 'string') {
                return null;
            }
            return <styles_1.Container>{events_1.getShortEventId(id)}</styles_1.Container>;
        },
    },
    'issue.id': {
        sortField: 'issue.id',
        renderFunc: function (data, _a) {
            var organization = _a.organization;
            var target = {
                pathname: "/organizations/" + organization.slug + "/issues/" + data['issue.id'] + "/",
            };
            return (<styles_1.Container>
          <styles_1.OverflowLink to={target} aria-label={data['issue.id']}>
            {data['issue.id']}
          </styles_1.OverflowLink>
        </styles_1.Container>);
        },
    },
    issue: {
        sortField: null,
        renderFunc: function (data, _a) {
            var organization = _a.organization;
            var issueID = data['issue.id'];
            if (!issueID) {
                return (<styles_1.Container>
            <styles_1.StyledShortId shortId={"" + data.issue}/>
          </styles_1.Container>);
            }
            var target = {
                pathname: "/organizations/" + organization.slug + "/issues/" + issueID + "/",
            };
            return (<styles_1.Container>
          <styles_1.OverflowLink to={target} aria-label={issueID}>
            <styles_1.StyledShortId shortId={"" + data.issue}/>
          </styles_1.OverflowLink>
        </styles_1.Container>);
        },
    },
    project: {
        sortField: 'project',
        renderFunc: function (data, _a) {
            var organization = _a.organization;
            return (<styles_1.Container>
          <projects_1.default orgId={organization.slug} slugs={[data.project]}>
            {function (_a) {
                    var projects = _a.projects;
                    var project = projects.find(function (p) { return p.slug === data.project; });
                    return (<projectBadge_1.default project={project ? project : { slug: data.project }} avatarSize={16}/>);
                }}
          </projects_1.default>
        </styles_1.Container>);
        },
    },
    user: {
        sortField: 'user',
        renderFunc: function (data) {
            if (data.user) {
                var _a = tslib_1.__read(data.user.split(':'), 2), key = _a[0], value = _a[1];
                var userObj = {
                    id: '',
                    name: '',
                    email: '',
                    username: '',
                    ip_address: '',
                };
                userObj[key] = value;
                var badge = <userBadge_1.default user={userObj} hideEmail avatarSize={16}/>;
                return <styles_1.Container>{badge}</styles_1.Container>;
            }
            return <styles_1.Container>{emptyValue}</styles_1.Container>;
        },
    },
    'user.display': {
        sortField: 'user.display',
        renderFunc: function (data) {
            if (data['user.display']) {
                var userObj = {
                    id: '',
                    name: data['user.display'],
                    email: '',
                    username: '',
                    ip_address: '',
                };
                var badge = <userBadge_1.default user={userObj} hideEmail avatarSize={16}/>;
                return <styles_1.Container>{badge}</styles_1.Container>;
            }
            return <styles_1.Container>{emptyValue}</styles_1.Container>;
        },
    },
    'count_unique(user)': {
        sortField: 'count_unique(user)',
        renderFunc: function (data) {
            var count = data.count_unique_user;
            if (typeof count === 'number') {
                return (<styles_1.FlexContainer>
            <styles_1.NumberContainer>
              <count_1.default value={count}/>
            </styles_1.NumberContainer>
            <styles_1.UserIcon size="20"/>
          </styles_1.FlexContainer>);
            }
            return <styles_1.Container>{emptyValue}</styles_1.Container>;
        },
    },
    release: {
        sortField: 'release',
        renderFunc: function (data) {
            return data.release ? (<styles_1.VersionContainer>
          <version_1.default version={data.release} anchor={false} tooltipRawVersion truncate/>
        </styles_1.VersionContainer>) : (<styles_1.Container>{emptyValue}</styles_1.Container>);
        },
    },
    'error.handled': {
        sortField: 'error.handled',
        renderFunc: function (data) {
            var values = data['error.handled'];
            // Transactions will have null, and default events have no handled attributes.
            if (values === null || (values === null || values === void 0 ? void 0 : values.length) === 0) {
                return <styles_1.Container>{emptyValue}</styles_1.Container>;
            }
            var value = Array.isArray(values) ? values.slice(-1)[0] : values;
            return <styles_1.Container>{[1, null].includes(value) ? 'true' : 'false'}</styles_1.Container>;
        },
    },
    key_transaction: {
        sortField: null,
        renderFunc: function (data, _a) {
            var _b;
            var organization = _a.organization;
            return (<styles_1.Container>
        <keyTransactionField_1.default isKeyTransaction={((_b = data.key_transaction) !== null && _b !== void 0 ? _b : 0) !== 0} organization={organization} projectSlug={data.project} transactionName={data.transaction}/>
      </styles_1.Container>);
        },
    },
    team_key_transaction: {
        sortField: null,
        renderFunc: function (data, _a) {
            var _b;
            var organization = _a.organization;
            return (<styles_1.Container>
        <teamKeyTransactionField_1.default isKeyTransaction={((_b = data.team_key_transaction) !== null && _b !== void 0 ? _b : 0) !== 0} organization={organization} projectSlug={data.project} transactionName={data.transaction}/>
      </styles_1.Container>);
        },
    },
    'trend_percentage()': {
        sortField: 'trend_percentage()',
        renderFunc: function (data) { return (<styles_1.NumberContainer>
        {typeof data.trend_percentage === 'number'
                ? formatters_1.formatPercentage(data.trend_percentage - 1)
                : emptyValue}
      </styles_1.NumberContainer>); },
    },
    'timestamp.to_hour': {
        sortField: 'timestamp.to_hour',
        renderFunc: function (data) { return (<styles_1.Container>
        {getDynamicText_1.default({
                value: <styles_1.StyledDateTime date={data['timestamp.to_hour']} format="lll z"/>,
                fixed: 'timestamp.to_hour',
            })}
      </styles_1.Container>); },
    },
    'timestamp.to_day': {
        sortField: 'timestamp.to_day',
        renderFunc: function (data) { return (<styles_1.Container>
        {getDynamicText_1.default({
                value: <styles_1.StyledDateTime date={data['timestamp.to_day']} dateOnly utc/>,
                fixed: 'timestamp.to_day',
            })}
      </styles_1.Container>); },
    },
};
/**
 * "Special functions" are functions whose values either do not map 1:1 to a single column,
 * or they require custom UI formatting that can't be handled by the datatype formatters.
 */
var SPECIAL_FUNCTIONS = {
    user_misery: function (fieldName) { return function (data) {
        var userMiseryField = fieldName;
        if (!(userMiseryField in data)) {
            return <styles_1.NumberContainer>{emptyValue}</styles_1.NumberContainer>;
        }
        var userMisery = data[userMiseryField];
        if (userMisery === null || isNaN(userMisery)) {
            return <styles_1.NumberContainer>{emptyValue}</styles_1.NumberContainer>;
        }
        var projectThresholdConfig = 'project_threshold_config';
        var countMiserableUserField = '';
        var miseryLimit = parseInt(userMiseryField.split('_').pop() || '', 10);
        if (isNaN(miseryLimit)) {
            countMiserableUserField = 'count_miserable_user';
            if (projectThresholdConfig in data) {
                miseryLimit = data[projectThresholdConfig][1];
            }
            else {
                miseryLimit = undefined;
            }
        }
        else {
            countMiserableUserField = "count_miserable_user_" + miseryLimit;
        }
        var uniqueUsers = data.count_unique_user;
        var miserableUsers;
        if (countMiserableUserField in data) {
            var countMiserableMiseryLimit = parseInt(countMiserableUserField.split('_').pop() || '', 10);
            miserableUsers =
                countMiserableMiseryLimit === miseryLimit ||
                    (isNaN(countMiserableMiseryLimit) && projectThresholdConfig)
                    ? data[countMiserableUserField]
                    : undefined;
        }
        return (<styles_1.BarContainer>
        <userMisery_1.default bars={10} barHeight={20} miseryLimit={miseryLimit} totalUsers={uniqueUsers} userMisery={userMisery} miserableUsers={miserableUsers}/>
      </styles_1.BarContainer>);
    }; },
};
/**
 * Get the sort field name for a given field if it is special or fallback
 * to the generic type formatter.
 */
function getSortField(field, tableMeta) {
    if (SPECIAL_FIELDS.hasOwnProperty(field)) {
        return SPECIAL_FIELDS[field].sortField;
    }
    if (!tableMeta) {
        return field;
    }
    if (fields_1.isEquation(field)) {
        return field;
    }
    for (var alias in fields_1.AGGREGATIONS) {
        if (field.startsWith(alias)) {
            return fields_1.AGGREGATIONS[alias].isSortable ? field : null;
        }
    }
    var fieldType = tableMeta[field];
    if (FIELD_FORMATTERS.hasOwnProperty(fieldType)) {
        return FIELD_FORMATTERS[fieldType].isSortable
            ? field
            : null;
    }
    return null;
}
exports.getSortField = getSortField;
var isDurationValue = function (data, field) {
    return field in data && typeof data[field] === 'number';
};
var spanOperationRelativeBreakdownRenderer = function (data, _a) {
    var _b, _c;
    var location = _a.location, organization = _a.organization, eventView = _a.eventView;
    var sumOfSpanTime = fields_1.SPAN_OP_BREAKDOWN_FIELDS.reduce(function (prev, curr) { return (isDurationValue(data, curr) ? prev + data[curr] : prev); }, 0);
    var cumulativeSpanOpBreakdown = Math.max(sumOfSpanTime, data['transaction.duration']);
    if (!isDurationValue(data, 'spans.total.time') ||
        fields_1.SPAN_OP_BREAKDOWN_FIELDS.every(function (field) { return !isDurationValue(data, field); }) ||
        cumulativeSpanOpBreakdown === 0) {
        return FIELD_FORMATTERS.duration.renderFunc(fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD, data);
    }
    var otherPercentage = 1;
    var orderedSpanOpsBreakdownFields;
    var sortingOnField = (_c = (_b = eventView === null || eventView === void 0 ? void 0 : eventView.sorts) === null || _b === void 0 ? void 0 : _b[0]) === null || _c === void 0 ? void 0 : _c.field;
    if (sortingOnField && fields_1.SPAN_OP_BREAKDOWN_FIELDS.includes(sortingOnField)) {
        orderedSpanOpsBreakdownFields = tslib_1.__spreadArray([
            sortingOnField
        ], tslib_1.__read(fields_1.SPAN_OP_BREAKDOWN_FIELDS.filter(function (op) { return op !== sortingOnField; })));
    }
    else {
        orderedSpanOpsBreakdownFields = fields_1.SPAN_OP_BREAKDOWN_FIELDS;
    }
    return (<RelativeOpsBreakdown>
      {orderedSpanOpsBreakdownFields.map(function (field) {
            var _a;
            if (!isDurationValue(data, field)) {
                return null;
            }
            var operationName = (_a = fields_1.getSpanOperationName(field)) !== null && _a !== void 0 ? _a : 'op';
            var spanOpDuration = data[field];
            var widthPercentage = spanOpDuration / cumulativeSpanOpBreakdown;
            otherPercentage = otherPercentage - widthPercentage;
            if (widthPercentage === 0) {
                return null;
            }
            return (<div key={operationName} style={{ width: utils_1.toPercent(widthPercentage || 0) }}>
            <tooltip_1.default title={<div>
                  <div>{operationName}</div>
                  <div>
                    <duration_1.default seconds={spanOpDuration / 1000} fixedDigits={2} abbreviation/>
                  </div>
                </div>} containerDisplayMode="block">
              <RectangleRelativeOpsBreakdown spanBarHatch={false} style={{
                    backgroundColor: utils_1.pickBarColour(operationName),
                    cursor: 'pointer',
                }} onClick={function (event) {
                    event.stopPropagation();
                    var filter = filter_1.stringToFilter(operationName);
                    if (filter === filter_1.SpanOperationBreakdownFilter.None) {
                        return;
                    }
                    analytics_1.trackAnalyticsEvent({
                        eventName: 'Performance Views: Select Relative Breakdown',
                        eventKey: 'performance_views.relative_breakdown.selection',
                        organization_id: parseInt(organization.id, 10),
                        action: filter,
                    });
                    react_router_1.browserHistory.push({
                        pathname: location.pathname,
                        query: tslib_1.__assign(tslib_1.__assign({}, location.query), filter_1.filterToLocationQuery(filter)),
                    });
                }}/>
            </tooltip_1.default>
          </div>);
        })}
      <div key="other" style={{ width: utils_1.toPercent(otherPercentage || 0) }}>
        <tooltip_1.default title={<div>{locale_1.t('Other')}</div>} containerDisplayMode="block">
          <OtherRelativeOpsBreakdown spanBarHatch={false}/>
        </tooltip_1.default>
      </div>
    </RelativeOpsBreakdown>);
};
var RelativeOpsBreakdown = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: flex;\n"], ["\n  position: relative;\n  display: flex;\n"])));
var RectangleRelativeOpsBreakdown = styled_1.default(rowBar_1.RowRectangle)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  width: 100%;\n"], ["\n  position: relative;\n  width: 100%;\n"])));
var OtherRelativeOpsBreakdown = styled_1.default(RectangleRelativeOpsBreakdown)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n"], ["\n  background-color: ", ";\n"])), function (p) { return p.theme.gray100; });
/**
 * Get the field renderer for the named field and metadata
 *
 * @param {String} field name
 * @param {object} metadata mapping.
 * @returns {Function}
 */
function getFieldRenderer(field, meta) {
    if (SPECIAL_FIELDS.hasOwnProperty(field)) {
        return SPECIAL_FIELDS[field].renderFunc;
    }
    if (fields_1.isRelativeSpanOperationBreakdownField(field)) {
        return spanOperationRelativeBreakdownRenderer;
    }
    var fieldName = fields_1.getAggregateAlias(field);
    var fieldType = meta[fieldName];
    for (var alias in SPECIAL_FUNCTIONS) {
        if (fieldName.startsWith(alias)) {
            return SPECIAL_FUNCTIONS[alias](fieldName);
        }
    }
    if (FIELD_FORMATTERS.hasOwnProperty(fieldType)) {
        return partial_1.default(FIELD_FORMATTERS[fieldType].renderFunc, fieldName);
    }
    return partial_1.default(FIELD_FORMATTERS.string.renderFunc, fieldName);
}
exports.getFieldRenderer = getFieldRenderer;
/**
 * Get the field renderer for the named field only based on its type from the given
 * metadata.
 *
 * @param {String} field name
 * @param {object} metadata mapping.
 * @returns {Function}
 */
function getFieldFormatter(field, meta) {
    var fieldName = fields_1.getAggregateAlias(field);
    var fieldType = meta[fieldName];
    if (FIELD_FORMATTERS.hasOwnProperty(fieldType)) {
        return partial_1.default(FIELD_FORMATTERS[fieldType].renderFunc, fieldName);
    }
    return partial_1.default(FIELD_FORMATTERS.string.renderFunc, fieldName);
}
exports.getFieldFormatter = getFieldFormatter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=fieldRenderers.jsx.map