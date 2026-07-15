<!-- markdownlint-disable-next-line -->
<div align="center">

  <!-- markdownlint-disable-next-line -->

# CV Tools

A tool to automate the creation of professional LaTeX-based CVs.

![LaTeX](https://img.shields.io/badge/latex-%23008080.svg?style=for-the-badge&logo=latex&logoColor=white)
![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge&logo=groq&logoColor=white)

![cover photo](docs/img/cover.png)

</div>

CV Tools is a project designed to streamline the creation of professional CVs using LaTeX. This tool provides templates and configuration files to easily generate a CV with customizable sections for education, work experience, publications, and much more.

Feel free to edit and use this tool according to your needs. Customize the LaTeX templates and configuration files to fit your personal requirements and preferences.

# Features

- **Customizable LaTeX Templates**: Pre-defined LaTeX templates for creating professional CVs.
- **Flexible Configuration**: Easy-to-edit configuration files to personalize your CV.
- **BibTeX Support**: Automatically generate a formatted list of publications from a BibTeX file.
- **Automated Build Process**: Scripted build process to generate the final PDF CV.
- **LLM Integration**: AI-powered personalization using Groq or OpenRouter APIs.
- **Experience Enhancement**: Automatically improve experience bullets with quantifiable achievements.
- **Professional Profile Generation**: AI-generated personalized professional summaries.
- **Multi-API Support**: Choose between Groq and OpenRouter for LLM processing.

# Build Status

| Ubuntu                                                                                     | macOS                                                                                    |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| ![Ubuntu Build](https://github.com/mlsdpk/cv-tools/actions/workflows/ubuntu.yml/badge.svg) | ![macOS Build](https://github.com/mlsdpk/cv-tools/actions/workflows/macos.yml/badge.svg) |

# Table of Contents

- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [LLM Integration](#llm-integration)
  - [Overview](#llm-overview)
  - [API Providers](#api-providers)
  - [Environment Setup](#environment-setup)
  - [LLM Features](#llm-features)
  - [Usage Examples](#llm-usage-examples)
- [YAML Configuration](#yaml-configuration)
  - [Heading](#heading)
  - [Subheading](#subheading)
  - [Sections](#sections)
  - [Using Special Characters](#using-special-characters)
- [BibTeX Configuration](#bibtex-configuration)
- [Contributing](#contributing)

# Getting Started

Below are two installation methods to set up and use CV Tools on your local machine. The Docker-based setup is recommended for a hassle-free experience. Alternatively, you can set up the tool manually from the source, which offers flexibility to either compile the PDF locally or generate the .tex file and use an external LaTeX renderer like [Overleaf](https://www.overleaf.com).

## Installation

### Method 1: Using Docker (Recommended)

Using docker allows you to run the tool in a consistent environment without worrying about dependencies on your local machine.

#### Prerequisites

- **Docker**: Ensure you have Docker installed on your machine. You can download and install Docker from [here](https://docs.docker.com/engine/install/).

#### Steps

Clone the Repository:

```bash
$ git clone https://github.com/mlsdpk/cv-tools.git
$ cd cv-tools
```

Build the Docker image using the provided `Dockerfile`.

```bash
$ docker build -t cv-tools .
```

Start a Docker container with the image you just built. This will launch an interactive shell with the virtual environment activated and mount the current cv-tools directory.

```bash
$ docker run -it -v $(pwd):/workdir cv-tools
```

for windows systems:
```bash
$ docker run -it -v $(pwd -W):/workdir cv-tools
```

The `-v $(pwd):/workdir` option mounts your local cv-tools directory to the `/workdir` directory inside the container.

### Method 2: From Source with Manual Installation

If you prefer to set up the environment manually on your local machine, follow the steps below. This method offers two options:

1. Use an external LaTeX renderer (e.g., [Overleaf](https://www.overleaf.com)) to compile the .tex file.
2. Install a LaTeX engine locally and generate the PDF directly.

#### Prerequisites

- **Option 1: External LaTeX Renderer**

  No LaTeX distribution is needed. You can generate the .tex file and upload it to tools like [Overleaf](https://www.overleaf.com).

- **Option 2: Local LaTeX Setup**

  Ensure you have a LaTeX distribution installed, such as [TeX Live](https://www.tug.org/texlive/) (recommended) or [MikTeX](https://miktex.org/).

- **Python**: Python 3.x is required for running the build scripts.

#### Installing Dependencies

Clone the Repository:

```bash
$ git clone https://github.com/mlsdpk/cv-tools.git
$ cd cv-tools
```

Set up a Python virtual environment and install dependencies:

```bash
$ python3 -m venv cv-tools
$ source cv-tools/bin/activate
$ pip install --require-hashes -r requirements.lock
```

#### LLM Setup (Optional)

If you plan to use AI-powered features, configure your API keys:

1. **Create `.env` file:**
   ```bash
   $ cp .env.example .env  # If example exists, or create manually
   ```

2. **Add your API keys to `.env`:**
   ```bash
   # Choose your provider
   API_PROVIDER="groq"  # or "openrouter"

   # Add your API keys
   GROQ_API_KEY="your-groq-key-here"
   OPENROUTER_API_KEY="your-openrouter-key-here"
   ```

3. **Create job offer file:**
   ```bash
   $ cp config/job_offer.txt.example config/job_offer.txt
   # Edit config/job_offer.txt with your target job description
   ```

If you plan to use Option 2 (Local LaTeX Setup), ensure all required LaTeX packages are installed. The necessary packages are listed in the `packages.list` file.

You can use the tlmgr command to install the packages as follows:

```bash
$ tlmgr install <package1> <package2> ...
```

**Note:** If you plan to use LLM features with the OpenRouter API, the `requests` library is required and is included in `requirements.txt`.

## Usage

To generate a CV, you can use the provided shell script, which offers flexibility through various command-line options.

## Default CV Generation

Running the script without any options will generate the CV using the default configuration (`cv.yaml`) located in the `config` directory.

```bash
$ ./run.sh
```

This command will also check and install all necessary dependencies before generating a `.tex` file and a PDF file, both of which will be saved in the `output` directory.

## LLM-Enhanced CV Generation

CV Tools supports AI-powered personalization using Large Language Models. You can enhance your CV with job-specific content using the following options:

### Professional Profile Generation

Generate an AI-crafted professional summary tailored to your target job:

```bash
$ ./run.sh --llm --job-offer config/job_offer.txt
```

### Experience Bullet Enhancement

Automatically improve your experience descriptions with quantifiable achievements:

```bash
$ ./run.sh --enhance-experience --job-offer config/job_offer.txt
```

### Combined LLM Features

Use both profile generation and experience enhancement together:

```bash
$ ./run.sh --llm --enhance-experience --job-offer config/job_offer.txt
```

### For Users Without a LaTeX Engine Installed

> Note: If you are using the Docker-based setup, you can ignore this section as the PDF will be generated within the container automatically.

If you don’t have a LaTeX engine installed locally, you can use the `--tex-only` option to generate the files required for an external LaTeX renderer:

```bash
$ ./run.sh --tex-only
```

This will generate the following files in the output directory:

- `output.tex`: The main LaTeX source file.
- `resume.cls`: The LaTeX class file required to compile the CV.

Upload both files to an external LaTeX renderer such as [Overleaf](https://www.overleaf.com) to produce the final PDF.

## Customize the CV Generation

You can customize the CV generation by specifying different configuration files, as well as changing the output file location.

- **Specify a different YAML configuration file:**
  ```bash
  $ ./run.sh -c path/to/custom_config.yaml
  ```
- **Change the output file location:**
  ```bash
  $ ./run.sh -o path/to/output/custom_cv.tex
  ```

These options can be combined together as well to suit your needs.

You can customize the content of your CV by editing the YAML configuration file. By default, this is the `cv.yaml` file located in the `config` directory, but you can specify a different YAML file from any location. This file allows you to define your personal details, education, work experience, skills, and more. You can add or remove sections, modify the fields, and tailor the CV content to your specific needs. The supported section types include `education`, `experience`, `skills`, `bullets`, `talks`, and `publications`. For more information, refer to [YAML Configuration](#yaml-configuration) section.

This tool also supports to automatically list your publications based on BibTeX entries provided in a specified BibTeX file. By default, this is the `publications.bib` file located in the `config` directory, but you can use a different BibTeX file from any location. Refer to [BibTeX Configuration](#bibtex-configuration) section for more details on configuring BibTeX entries.

## Skipping Dependency Checks and Installations

If you already have all dependencies installed and want to skip the automatic checking and installation process, use the `--no-deps` option:

```bash
$ ./run.sh --no-deps
```

This option is useful for speeding up subsequent runs when you know that all dependencies are already satisfied.

# LLM Integration

CV Tools now includes powerful AI-powered features to enhance your resume with personalized content using Large Language Models (LLMs). This integration helps create more compelling and job-specific resumes by analyzing job requirements and tailoring your experience descriptions accordingly.

## LLM Overview

The LLM integration provides two main enhancements:

1. **Professional Profile Generation**: AI creates a personalized professional summary based on your CV and the target job description
2. **Experience Bullet Enhancement**: AI rewrites your experience bullets to emphasize job-relevant skills and add quantifiable achievements

## API Providers

CV Tools supports two LLM API providers:

### Groq
- **Default Provider**: Fast inference with models like `openai/gpt-oss-120b`
- **Setup**: Requires `GROQ_API_KEY` in `.env` file
- **Best for**: Cost-effective, fast processing

### OpenRouter
- **Alternative Provider**: Access to multiple models including GPT-4, Claude, and others
- **Setup**: Requires `OPENROUTER_API_KEY` in `.env` file
- **Best for**: Advanced models, flexibility

## Environment Setup

### 1. Choose Your API Provider

Create or edit the `.env` file in your project root:

```bash
# For Groq (default)
API_PROVIDER="groq"
GROQ_API_KEY="your-groq-api-key-here"

# OR for OpenRouter
API_PROVIDER="openrouter"
OPENROUTER_API_KEY="your-openrouter-api-key-here"
```

### 2. API Key Acquisition

**Groq API Key:**
- Visit [Groq Console](https://console.groq.com/)
- Create an account and generate an API key
- Add to `.env` as `GROQ_API_KEY`

**OpenRouter API Key:**
- Visit [OpenRouter](https://openrouter.ai/)
- Sign up and get your API key
- Add to `.env` as `OPENROUTER_API_KEY`

### 3. Job Offer File

Create a job offer file (e.g., `config/job_offer.txt`) containing the job description you want to target:

```
# Job Responsibilities

- Efficiently utilize (Unify+) to organize data, create reporting dashboards, analyze results, and deliver business insights.
- Contribute to a queue of project requests that involve recurring reporting, overlapping deadlines, and shifting project scopes.
- Derive insights that help frame up and add value to Circana data.
- Present findings in internal touch-bases and collaborative meetings.
```

## LLM Features

### Professional Profile Generation

Automatically generates a compelling 2-paragraph professional summary that:
- Highlights your most relevant experience and skills
- Aligns with the target job requirements
- Uses industry-specific keywords
- Maintains professional tone and first-person perspective

**Example Output:**
```
Mechanical engineer with 5+ years of experience in energy systems modeling and data analysis. Specialized in developing TIMES framework scenarios for national energy transitions and quantifying corporate carbon footprints using GHG Protocol methodology.

Expert in Python-based analytical tools, Google Cloud Platform, and advanced AI technologies including LlamaIndex and NLP models. Proven track record in leading cross-functional teams to deliver strategic insights for energy sector clients, with particular expertise in Latin American market dynamics.
```

### Experience Bullet Enhancement

Transforms generic experience descriptions into impactful, quantifiable achievements:
- Identifies job-relevant skills and experiences
- Adds specific metrics and measurable outcomes
- Incorporates industry keywords naturally
- Maintains authenticity (never fabricates information)

**Before:**
```
- Developed software solutions
- Managed project teams
- Improved system performance
```

**After:**
```
- Developed cloud-based analytics platform using Python, reducing data processing time by 40%
- Led cross-functional team of 5 developers in agile methodology, delivering projects 25% under budget
- Optimized database queries and system architecture, improving overall performance by 35%
```

## LLM Usage Examples

### Basic LLM Profile Generation

```bash
# Generate CV with AI-enhanced professional profile
./run.sh --llm --job-offer config/job_offer.txt
```

### Experience Bullet Enhancement

```bash
# Enhance experience bullets with AI
./run.sh --enhance-experience --job-offer config/job_offer.txt
```

### Combined Features

```bash
# Use both LLM features together
./run.sh --llm --enhance-experience --job-offer config/job_offer.txt
```

### Custom Configuration

```bash
# Use custom config and output files
./run.sh -c config/my_cv.yaml -o output/my_cv.tex --llm --enhance-experience --job-offer config/senior_role.txt
```

## LLM Best Practices

### Content Guidelines
- **Authenticity**: LLM enhancements are based only on information in your CV
- **Relevance**: Always provide a job offer file for best results
- **Review**: Always review AI-generated content before final use
- **Customization**: Use the generated content as a starting point for further personalization

### Performance Tips
- **Job-Specific Files**: Create separate job offer files for different applications
- **Version Control**: Keep multiple versions of your CV for different roles
- **API Selection**: Use Groq for faster processing, OpenRouter for advanced models
- **Cost Management**: Monitor API usage, especially with OpenRouter

### Troubleshooting

**Common Issues:**
- **Missing API Key**: Ensure correct API key in `.env` file
- **Invalid Job File**: Verify job offer file exists and contains relevant content
- **API Limits**: Check API provider limits and billing

**Fallback Behavior:**
- If LLM fails, original content is used
- System continues with standard generation
- Error messages guide troubleshooting

### Unicode Character Handling

The system automatically cleans Unicode characters from LLM responses to prevent LaTeX compilation errors:
- Converts problematic Unicode spaces (U+202F) to regular spaces
- Replaces special quotes and dashes with LaTeX-compatible equivalents
- **Escapes ampersands (&) to \&** for proper LaTeX table compatibility
- Removes or replaces non-ASCII characters that cause compilation issues
- Maintains readability while ensuring LaTeX compatibility

# YAML Configuration

The YAML configuration file allows you to customize various aspects of your CV. This section provides detailed instructions on configuring each parameter, including the `heading`, `subheading`, and `sections` fields. Each parameter controls different parts of the CV layout and content.

## Heading

The `heading` parameter sets the main title of the CV.
| Field | Type | Description | Required |
|-------|------|-------------|-----------|
| `name` | string | The name of the author, displayed as the main heading. | Yes |
| `language` | string | The language of the CV. Supported values are `en` (English) and `es` (Spanish). Defaults to `en`. | No |

Example:

```yaml
heading:
  name: "John Doe" # The name of the CV author
  language: "en"
```

## Subheading

The `subheading` parameter allows you to add supplementary details below the main heading. This includes personal links and social media profiles, which are displayed on one or two lines depending on the configuration.

### Links

The `links` type includes personal URLs or contact details. They can be highlighted and placed either on the first or second line.

| Field        | Type    | Description                                                                        | Required |
| ------------ | ------- | ---------------------------------------------------------------------------------- | -------- |
| `type`       | string  | Type of the subheading content; set to `links` for URLs or contact details.        | No       |
| `content`    | array   | List of link objects. Each object includes: `name`, `highlight`, and `show_below`. | No       |
| `name`       | string  | The URL or contact detail.                                                         | No       |
| `highlight`  | boolean | Whether or not the link should be highlighted and clickable.                       | No       |
| `show_below` | boolean | Determines if the link should be on the first line (false) or second line (true).  | No       |

### Socials

The `socials` type includes links to social media profiles and are rendered as icons. Supported types are:

- `orcid_id`
- `linkedin`
- `github`
- `twitter`

| Field        | Type    | Description                                                                              | Required |
| ------------ | ------- | ---------------------------------------------------------------------------------------- | -------- |
| `type`       | string  | Type of the subheading content; set to socials for social media profiles.                | No       |
| `content`    | array   | List of social objects. Each object includes: `type`, `url`, and `show_below`.           | No       |
| `type`       | string  | Type of social link (`orcid_id`, `linkedin`, `github` or `twitter`).                     | No       |
| `url`        | string  | The URL or ID of the social profile.                                                     | No       |
| `show_below` | boolean | Determines if the social link should be on the first line (false) or second line (true). | No       |

Example:

```yaml
subheading:
  - type: links
    content:
      - name: "https://www.johndoeportfolio.com"
        highlight: true
        show_below: false
      - name: "johndoe@email.com"
        highlight: false
        show_below: true
  - type: socials
    content:
      - type: orcid_id
        url: "0000-0000-0000-0000"
        show_below: false
      - type: linkedin
        url: "https://linkedin.com/in/johndoe"
        show_below: false
```

![subheading-section](docs/img/subheading-section.png)

## Sections

The `sections` parameter allows you to define different sections of your CV, each designed to represent a specific kind of information. Below is a table summarizing the supported section types:

| Key            | Description                                             |
| -------------- | ------------------------------------------------------- |
| `education`    | Lists academic qualifications and related details.      |
| `experience`   | Details professional experiences.                       |
| `bullets`      | Provides a list of items and optional subitems.         |
| `skills`       | Lists skills, languages, tools, and technologies.       |
| `talks`        | Lists talks, workshops, and lectures given.             |
| `publications` | Lists research papers, articles, or other publications. |
| `newpage`      | Inserts a new page in the CV.                           |
| `professional_profile` | Provides a brief summary of your professional background and skills. |

Each section type has specific fields and formatting rules. Below are detailed descriptions and example YAML configurations for each section type.

### 1. Education

The `education` section is used to list your academic qualifications.

| Key       | Type   | Description                  | Required |
| --------- | ------ | ---------------------------- | -------- |
| `type`    | string | Must be `education`.         | Yes      |
| `content` | list   | List of education entries.   | Yes      |

**Education Entry**

| Key      | Type   | Description                                                                                             | Required |
| -------- | ------ | ------------------------------------------------------------------------------------------------------- | -------- |
| `name`   | string | Title of the education section.                                                                         | Yes      |
| `entity` | list   | List of education entities. This is used to group relevant educational experiences under a single section. | Yes      |

**Education Entity**

| Field          | Type   | Description                                     | Required |
| -------------- | ------ | ----------------------------------------------- | -------- |
| `university`   | string | The name of the university or institution.      | Yes      |
| `location`     | string | The location of the university or institution.  | Yes      |
| `dates`        | string | The period during which the degree was pursued. | Yes      |
| `degree`       | string | The name of the degree obtained.                | Yes      |
| `honors`       | string | Honors received, if any.                        | No       |
| `thesis_title` | string | Title of the thesis, if applicable.             | No       |
| `supervisor`   | string | Name of the supervisor, if applicable.          | No       |

Example:

```yaml
sections:
  - type: education
    content:
      - name: "Education"
        entity:
          - university: "Fictional University"
            location: "Imaginaria, Wonderland"
            dates: "September 2021 - June 2024"
            degree: "Bachelor of Science in Computer Science"
            honors: "Magna Cum Laude"
            thesis_title: "An Exploration of Quantum Computing in Virtual Environments"
            supervisor: "Dr. Alice Wonder"
          - university: "Imaginary Institute of Technology"
            location: "Nowhere City, Utopia"
            dates: "August 2018 - May 2021"
            degree: "Associate Degree in Artificial Intelligence"
            supervisor: "Dr. Bob Builder"
```

![education-section](docs/img/education-section.png)

### 2. Experience

The `experience` section is used to detail your professional experiences and releated details.

| Key       | Type   | Description                 | Required |
| --------- | ------ | --------------------------- | -------- |
| `type`    | string | Must be `experience`.       | Yes      |
| `content` | list   | List of experience entries. | Yes      |

**Experience Entry**

| Key      | Type   | Description                                                                                         | Required |
| -------- | ------ | --------------------------------------------------------------------------------------------------- | -------- |
| `name`   | string | Title of the experience section.                                                                    | Yes      |
| `entity` | list   | List of experience entities. This is used to group relevant experiences together under one section. | Yes      |

**Experience Entity**

| Key                | Type   | Description                               | Required |
| ------------------ | ------ | ----------------------------------------- | -------- |
| `organization`     | string | Name of the organization or company.      | Yes      |
| `dates`            | string | Duration of employment or involvement.    | Yes      |
| `position`         | string | Position or role held.                    | Yes      |
| `responsibilities` | list   | List of responsibilities or achievements. | No       |
| `supervisor`       | string | Supervisor's name (optional).             | No       |
| `department`       | string | Department name (optional).               | No       |
| `location`         | string | Location of the organization (optional).  | No       |

Example:

```yaml
- type: experience
  content:
    - name: "Professional Experience"
      entity:
        - organization: "Tech Innovations Inc."
          dates: "July 2024 - Present"
          position: "Software Engineer"
          responsibilities:
            - "Developed and maintained cloud-based solutions for various enterprise clients."
            - "Led a team of developers in designing scalable software architectures."
            - "Improved system performance by 30% through code optimization and database restructuring."
        - organization: "NextGen Robotics"
          dates: "June 2022 - June 2024"
          position: "Robotics Engineer"
          responsibilities:
            - "Designed and implemented autonomous navigation systems for industrial robots."
            - "Collaborated with cross-functional teams to integrate machine learning models into robotic platforms."
```

![experience-section](docs/img/experience-section.png)

### 3. Bullets

| Key           | Description                                  |
| ------------- | -------------------------------------------- |
| `type`        | Must be `bullets`.                           |
| `title`       | Title of the bullet section.                 |
| `description` | Description or introductory text (optional). |
| `content`     | List of bullet points.                       |

**Bullet Item**

| Key        | Description                                               |
| ---------- | --------------------------------------------------------- |
| `item`     | Main bullet point text.                                   |
| `subitems` | List of sub-bullet points under the main item (optional). |

Example:

```yaml
- type: bullets
  title: "Honors and Awards"
  description: ""
  content:
    - item: "Dean's List (2023, 2022)"
    - item: "Best Paper Award at Tech Innovations Conference (2023)"
    - item: "Outstanding Graduate Award, Fictional University (2024)"
```

![bullets-section-1](docs/img/bullets-section-1.png)

```yaml
- type: bullets
  title: "Professional Activities"
  description: "Served/ing as a reviewer for"
  content:
    - item: "Journals"
      subitems:
        - "Journal of Artificial Intelligence Research (JAIR)"
        - "Journal of Machine Learning Research (JMLR)"
    - item: "Conferences"
      subitems:
        - "IEEE Conference on Computer Vision and Pattern Recognition (CVPR)"
        - "International Conference on Learning Representations (ICLR)"
```

![bullets-section-2](docs/img/bullets-section-2.png)

### 4. Skills

The `skills` section is used to list your skills, languages, tools, and technologies.

| Key       | Type   | Description            | Required |
| --------- | ------ | ---------------------- | -------- |
| `type`    | string | Must be `skills`.      | Yes      |
| `content` | list   | List of skill entries. | Yes      |

**Skills Entry**

| Key      | Type   | Description                                                                               | Required |
| -------- | ------ | ----------------------------------------------------------------------------------------- | -------- |
| `name`   | string | Title of the skills section.                                                              | Yes      |
| `entity` | list   | List of skill entities. This is used to group relevant skills together under a single section. | Yes      |

**Skills Entity**

| Key    | Type   | Description                     | Required |
| ------ | ------ | ------------------------------- | -------- |
| `name` | string | Title of the skills category.   | Yes      |
| `data` | string | List of skills or technologies. | Yes      |

Example:

```yaml
- type: skills
  content:
    - name: "Skills"
      entity:
        - name: "Spoken Languages"
          data: "English (Fluent), Spanish (Intermediate)"
        - name: "Programming Languages"
          data: "Python, Java, C++, SQL, JavaScript"
        - name: "Tools and Technologies"
          data: "AWS, Docker, Kubernetes, TensorFlow, Git, Jenkins, Linux, Jira"
```

![skills-section](docs/img/skills-section.png)

### 5. Talks

| Key       | Description                     |
| --------- | ------------------------------- |
| `type`    | Must be `talks`.                |
| `title`   | Title of the talks section.     |
| `content` | List of talks or presentations. |

**Talk Entry**

| Key     | Description                                                  |
| ------- | ------------------------------------------------------------ |
| `name`  | Title of the talk, type, conference or event name, location. |
| `month` | Month of the talk.                                           |
| `year`  | Year of the talk.                                            |

Example:

```yaml
- type: talks
  title: "Invited Talks/Workshops"
  content:
    - name: "``AI in Everyday Life'', Invited talk, Tech Conference 2023, Imaginaria."
      month: "Nov."
      year: "2023"
    - name: "``Cloud Computing for Beginners'', Workshop, FutureTech Expo 2022, Nowhere City."
      month: "Oct."
      year: "2022"
    - name: "``Robotics in Modern Industry'', Guest lecture, Imaginary Institute of Technology."
      month: "May"
      year: "2021"
    - name: "``Building Scalable Systems with Docker and Kubernetes'', Workshop, DevOps World 2023, Tech City."
      month: "Aug."
      year: "2023"
    - name: "``Ethics in AI'', Panel discussion, Ethics in Technology Conference 2022, Metropolis."
      month: "Sep."
      year: "2022"
```

![talks-section](docs/img/talks-section.png)

### 6. Publications

The `publications` section type is designed to list all relevant research articles, papers, patents and academic publications. This section automatically pulls data from a user-specified BibTeX file to render the publications in your CV. For more information on how to configure and link your BibTeX file, refer to the [BibTeX Configuration Section](#bibtex-configuration).

| Key       | Type   | Description                                                                           | Required |
| --------- | ------ | ------------------------------------------------------------------------------------- | -------- |
| `type`    | string | Must be `publications`. Specifies that the section will render academic publications. | Yes      |
| `title`   | string | Title of the publications section.                                                    | Yes      |
| `bibfile` | string | Path to the BibTeX file.                                                              | Yes      |

Example:

```yaml
sections:
  - type: publications
    title: "Publications"
    bibfile: publications.bib
```

### 7. New Page

The `newpage` section type is used to force the current page to end and start a new one. This can be useful when you want to ensure that certain sections or content start on a fresh page, particularly in situations where visual organization is important.

| Key    | Type   | Description                                                             | Required |
| ------ | ------ | ----------------------------------------------------------------------- | -------- |
| `type` | string | Must be `newpage`. Forces the current page to end and starts a new one. | Yes      |

Example:

```yaml
sections:
  - type: newpage
```

### 8. Professional Profile

The `professional_profile` section is used to provide a brief summary of your professional background and skills.

| Key       | Type   | Description                                                     | Required |
| --------- | ------ | --------------------------------------------------------------- | -------- |
| `type`    | string | Must be `professional_profile`.                                 | Yes      |
| `title`   | string | The title of the section (e.g., "Professional Profile").        | Yes      |
| `content` | string | A paragraph describing your professional profile.               | Yes      |

Example:

```yaml
sections:
  - type: professional_profile
    title: "Professional Profile"
    content: "A highly motivated and results-oriented software engineer with over 5 years of experience in developing and maintaining web applications. Proficient in Python, JavaScript, and various cloud technologies. Seeking to leverage my skills to contribute to a dynamic and innovative team."
```

An example of a complete YAML configuration can be found [here](config/cv.yaml).

## Using Special Characters

When configuring your YAML files, you might want to include special formatting within strings, such as bold text, hyperlinks, line breaks, and horizontal spacing. These special characters and formatting options will be automatically converted into the appropriate LaTeX commands during the rendering process. Here's how to use them:

### Supported Characters

- **Bold Text:**  
  To make text bold, wrap the text with `**` (e.g., `"**Bold Text**"`).

- **Italics:**  
  To italicize text, wrap the text with `*` (e.g., `"*Italic Text*"`).

- **Hyperlinks:**  
  To create a hyperlink, use the Markdown link syntax `[text](url)` (e.g., `"[My Portfolio](https://myportfolio.com)"`).

- **Line Breaks:**  
  To insert a line break, use the newline character `\n` (e.g., `"First Line\nSecond Line"`).

- **Horizontal Spacing:**

  - To add a small space, use two spaces (e.g., `"Text  2 spaces later"`).
  - To add an "em" space, use four spaces or a tab (e.g., `"Text    4 spaces later"` or `"Text\twith a tab"`).

- **Quotes**
  - Always use single quotes for quoted phrases (e.g., 'Data Science Club') to avoid issues with double quotes inside YAML.
  - cv-tools will automatically convert these into proper LaTeX-style double quotes (``like this'') during rendering.

Here’s an example YAML configuration that utilizes these special characters:

```yaml
heading:
  name: "John Doe" # mandatory

sections:
  - type: education
    content:
      - university: "Fictional University"
        location: "Imaginaria, Wonderland"
        dates: "September 2021 - June 2024"
        degree: "Bachelor of Science in *Computer Science*"
        honors: "**Magna Cum Laude**"
        thesis_title: "An Exploration of ['Quantum Computing'](https://en.wikipedia.org/wiki/Quantum_computing) in Virtual Environments"
        supervisor: "Dr. Alice Wonder"
```

![special-characters-section](docs/img/special-characters-section.png)

# BibTeX Configuration

Managing your publications is straightforward with a BibTeX file. The BibTeX file allows you to maintain a structured list of your publications, which can be automatically formatted and included in your CV.

![publications-section](docs/img/publications-section.png)

## Steps to Configure BibTeX:

1. **Create a BibTeX file:** Create a `.bib` file containing entries for your publications. The tool will automatically format these entries and include them in your CV.
2. **Add a `publications` section:** In your YAML configuration file, add a section with the type `publications`. Use the `title` field to name the section as desired.
3. **Specify the BibTeX file path:** In the `publications` section, set the `bibfile` field to the path of your BibTeX file.

**Example BibTeX Entry:**

> Note that cv-tools will automatically bold the author's name in publications if it matches the heading name.

> In most cases, BibTeX entries do not include the URL field. cv-tools will add the URL link at the end only if the entry contains a URL field. If you would like to include a link to your publication, please add the URL field to the BibTeX entry manually.

```bibtex
@article{doe2024quantum,
  author = {John Doe and Jane Smith and Alice Wonder},
  title = {Quantum Computing: Bridging the Gap Between Theory and Application},
  journal = {Journal of Computer Science},
  year = {2024},
  url = {https://example.com/quantum-computing-paper}
}
```

Your publications will be included in the CV in the order they appear in the .bib file. An example BibTeX data file is provided [here](config/publications.bib).


# Contributing

Feel free to contribute to this project by submitting issues or pull requests. Contributions are welcome to improve the templates, add new features, or fix bugs.

# Acknowledgments

The LaTeX template currently supported in this project is based on the **Medium Length Professional CV** template from [LaTeXTemplates.com](https://www.latextemplates.com/template/medium-length-professional-cv), which has been extensively modified for this project. The original template was created by [Trey Hunner](https://treyhunner.com).

# License

This project is licensed under the [MIT License](https://opensource.org/license/mit).
