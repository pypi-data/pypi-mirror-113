Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var capitalize_1 = tslib_1.__importDefault(require("lodash/capitalize"));
var styles_1 = require("app/components/charts/styles");
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var keyValueTable_1 = require("app/components/keyValueTable");
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var TagsTable = function (_a) {
    var event = _a.event, query = _a.query, generateUrl = _a.generateUrl, _b = _a.title, title = _b === void 0 ? locale_1.t('Tag Details') : _b;
    var eventWithMeta = metaProxy_1.withMeta(event);
    var tags = eventWithMeta.tags;
    var formatErrorKind = function (kind) {
        return capitalize_1.default(kind.replace(/_/g, ' '));
    };
    var getErrorMessage = function (error) {
        var _a;
        if (Array.isArray(error)) {
            if ((_a = error[1]) === null || _a === void 0 ? void 0 : _a.reason) {
                return formatErrorKind(error[1].reason);
            }
            else {
                return formatErrorKind(error[0]);
            }
        }
        return formatErrorKind(error);
    };
    var getTooltipTitle = function (errors) {
        return <TooltipTitle>{getErrorMessage(errors[0])}</TooltipTitle>;
    };
    return (<StyledTagsTable>
      <styles_1.SectionHeading>{title}</styles_1.SectionHeading>
      <keyValueTable_1.KeyValueTable>
        {tags.map(function (tag) {
            var _a, _b, _c;
            var tagInQuery = query.includes(tag.key + ":");
            var target = tagInQuery ? undefined : generateUrl(tag);
            var keyMetaData = metaProxy_1.getMeta(tag, 'key');
            var valueMetaData = metaProxy_1.getMeta(tag, 'value');
            var renderTagValue = function () {
                switch (tag.key) {
                    case 'release':
                        return <version_1.default version={tag.value} anchor={false} withPackage/>;
                    default:
                        return tag.value;
                }
            };
            return (<keyValueTable_1.KeyValueTableRow key={tag.key} keyName={((_a = keyMetaData === null || keyMetaData === void 0 ? void 0 : keyMetaData.err) === null || _a === void 0 ? void 0 : _a.length) ? (<tooltip_1.default title={getTooltipTitle(keyMetaData.err)}>
                    <i>{"<" + locale_1.t('invalid') + ">"}</i>
                  </tooltip_1.default>) : (tag.key)} value={((_b = valueMetaData === null || valueMetaData === void 0 ? void 0 : valueMetaData.err) === null || _b === void 0 ? void 0 : _b.length) ? (<tooltip_1.default title={getTooltipTitle(valueMetaData.err)}>
                    <i>{"<" + locale_1.t('invalid') + ">"}</i>
                  </tooltip_1.default>) : ((_c = keyMetaData === null || keyMetaData === void 0 ? void 0 : keyMetaData.err) === null || _c === void 0 ? void 0 : _c.length) ? (<span>{renderTagValue()}</span>) : tagInQuery ? (<tooltip_1.default title={locale_1.t('This tag is in the current filter conditions')}>
                    <span>{renderTagValue()}</span>
                  </tooltip_1.default>) : (<link_1.default to={target || ''}>{renderTagValue()}</link_1.default>)}/>);
        })}
      </keyValueTable_1.KeyValueTable>
    </StyledTagsTable>);
};
exports.default = TagsTable;
var StyledTagsTable = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(3));
var TooltipTitle = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=tagsTable.jsx.map