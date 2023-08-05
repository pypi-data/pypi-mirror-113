Object.defineProperty(exports, "__esModule", { value: true });
exports.getInitialData = exports.getFormFields = void 0;
var tslib_1 = require("tslib");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var debugFileSources_1 = require("app/data/debugFileSources");
var locale_1 = require("app/locale");
function objectToChoices(obj) {
    return Object.entries(obj).map(function (_a) {
        var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
        return [key, locale_1.t(value)];
    });
}
var commonFields = {
    id: {
        name: 'id',
        type: 'hidden',
        required: true,
        defaultValue: function () { return Math.random().toString(36).substring(2); },
    },
    name: {
        name: 'name',
        type: 'string',
        required: true,
        label: locale_1.t('Name'),
        placeholder: locale_1.t('New Repository'),
        help: locale_1.t('A display name for this repository'),
    },
    // filters are explicitly not exposed to the UI
    layoutType: {
        name: 'layout.type',
        type: 'select',
        label: locale_1.t('Directory Layout'),
        help: locale_1.t('The layout of the folder structure.'),
        defaultValue: 'native',
        choices: objectToChoices(debugFileSources_1.DEBUG_SOURCE_LAYOUTS),
    },
    layoutCasing: {
        name: 'layout.casing',
        type: 'select',
        label: locale_1.t('Path Casing'),
        help: locale_1.t('The case of files and folders.'),
        defaultValue: 'default',
        choices: objectToChoices(debugFileSources_1.DEBUG_SOURCE_CASINGS),
    },
    prefix: {
        name: 'prefix',
        type: 'string',
        label: 'Root Path',
        placeholder: '/',
        help: locale_1.t('The path at which files are located within this repository.'),
    },
    separator: {
        name: '',
        type: 'separator',
    },
};
var httpFields = {
    url: {
        name: 'url',
        type: 'url',
        required: true,
        label: locale_1.t('Download Url'),
        placeholder: 'https://msdl.microsoft.com/download/symbols/',
        help: locale_1.t('Full URL to the symbol server'),
    },
    username: {
        name: 'username',
        type: 'string',
        required: false,
        label: locale_1.t('User'),
        placeholder: 'admin',
        help: locale_1.t('User for HTTP basic auth'),
    },
    password: {
        name: 'password',
        type: 'string',
        required: false,
        label: locale_1.t('Password'),
        placeholder: 'open-sesame',
        help: locale_1.t('Password for HTTP basic auth'),
    },
};
var s3Fields = {
    bucket: {
        name: 'bucket',
        type: 'string',
        required: true,
        label: locale_1.t('Bucket'),
        placeholder: 's3-bucket-name',
        help: locale_1.t('Name of the S3 bucket. Read permissions are required to download symbols.'),
    },
    region: {
        name: 'region',
        type: 'select',
        required: true,
        label: locale_1.t('Region'),
        help: locale_1.t('The AWS region and availability zone of the bucket.'),
        choices: debugFileSources_1.AWS_REGIONS.map(function (_a) {
            var _b = tslib_1.__read(_a, 2), k = _b[0], v = _b[1];
            return [
                k,
                <span key={k}>
        <code>{k}</code> {v}
      </span>,
            ];
        }),
    },
    accessKey: {
        name: 'access_key',
        type: 'string',
        required: true,
        label: locale_1.t('Access Key ID'),
        placeholder: 'AKIAIOSFODNN7EXAMPLE',
        help: locale_1.tct('Access key to the AWS account. Credentials can be managed in the [link].', {
            link: (<externalLink_1.default href="https://console.aws.amazon.com/iam/">
            IAM console
          </externalLink_1.default>),
        }),
    },
    secretKey: {
        name: 'secret_key',
        type: 'string',
        required: true,
        label: locale_1.t('Secret Access Key'),
        placeholder: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    },
};
var gcsFields = {
    bucket: {
        name: 'bucket',
        type: 'string',
        required: true,
        label: locale_1.t('Bucket'),
        placeholder: 'gcs-bucket-name',
        help: locale_1.t('Name of the GCS bucket. Read permissions are required to download symbols.'),
    },
    clientEmail: {
        name: 'client_email',
        type: 'email',
        required: true,
        label: locale_1.t('Client Email'),
        placeholder: 'user@project.iam.gserviceaccount.com',
        help: locale_1.t('Email address of the GCS service account.'),
    },
    privateKey: {
        name: 'private_key',
        type: 'string',
        required: true,
        multiline: true,
        autosize: true,
        maxRows: 5,
        rows: 3,
        label: locale_1.t('Private Key'),
        placeholder: '-----BEGIN PRIVATE KEY-----\n[PRIVATE-KEY]\n-----END PRIVATE KEY-----',
        help: locale_1.tct('The service account key. Credentials can be managed on the [link].', {
            link: (<externalLink_1.default href="https://console.cloud.google.com/project/_/iam-admin">
          IAM &amp; Admin Page
        </externalLink_1.default>),
        }),
    },
};
function getFormFields(type) {
    switch (type) {
        case 'http':
            return [
                commonFields.id,
                commonFields.name,
                commonFields.separator,
                httpFields.url,
                httpFields.username,
                httpFields.password,
                commonFields.separator,
                commonFields.layoutType,
                commonFields.layoutCasing,
            ];
        case 's3':
            return [
                commonFields.id,
                commonFields.name,
                commonFields.separator,
                s3Fields.bucket,
                s3Fields.region,
                s3Fields.accessKey,
                s3Fields.secretKey,
                commonFields.separator,
                commonFields.prefix,
                commonFields.layoutType,
                commonFields.layoutCasing,
            ];
        case 'gcs':
            return [
                commonFields.id,
                commonFields.name,
                commonFields.separator,
                gcsFields.bucket,
                gcsFields.clientEmail,
                gcsFields.privateKey,
                commonFields.separator,
                commonFields.prefix,
                commonFields.layoutType,
                commonFields.layoutCasing,
            ];
        default:
            return undefined;
    }
}
exports.getFormFields = getFormFields;
function getInitialData(sourceConfig) {
    var _a;
    if (!sourceConfig) {
        return undefined;
    }
    if (sourceConfig.layout) {
        var layout = sourceConfig.layout, initialData = tslib_1.__rest(sourceConfig, ["layout"]);
        var casing = layout.casing, type = layout.type;
        return tslib_1.__assign(tslib_1.__assign({}, initialData), (_a = {}, _a['layout.casing'] = casing, _a['layout.type'] = type, _a));
    }
    return sourceConfig;
}
exports.getInitialData = getInitialData;
//# sourceMappingURL=utils.jsx.map